"""
Tests for Stage 3: TC Review Engine

Tests the ReviewEngine, ISTQBValidator, and domain plugins.
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tc_reviewer import ReviewConfig, ReviewEngine, Finding
from tc_reviewer.plugin_base import PluginManager, DomainPluginBase
from tc_reviewer.com_plugin import COMPlugin


class TestReviewEngine:
    """Test ReviewEngine functionality."""
    
    def test_init(self):
        """Test ReviewEngine initialization."""
        config = ReviewConfig(
            tc_v1_path=Path("output/enhanced_tc/test_tc.md"),
            feature_id="FGR-TEST-001",
            sw_package="SVR26A",
            rapp_name="COM",
        )
        
        engine = ReviewEngine(config)
        
        assert engine.config == config
        assert engine.evidence_store == []
        assert engine.findings == []
    
    def test_calculate_quality_score(self):
        """Test quality score calculation."""
        config = ReviewConfig(
            tc_v1_path=Path("output/enhanced_tc/test_tc.md"),
            feature_id="FGR-TEST-001",
            sw_package="SVR26A",
            rapp_name="COM",
        )
        
        engine = ReviewEngine(config)
        
        # No findings = 100 score
        score = engine._calculate_quality_score()
        assert score == 100.0
        
        # Add some findings
        engine.findings = [
            Finding(
                category="RC",
                check_id="RC-1",
                severity="High",
                description="Test finding",
                tc_section="Test",
                evidence_status="Partial",
            ),
            Finding(
                category="SC",
                check_id="SC-1",
                severity="Medium",
                description="Test finding 2",
                tc_section="Test",
                evidence_status="Partial",
            ),
        ]
        
        score = engine._calculate_quality_score()
        assert 0 <= score <= 100
    
    def test_assess_risk(self):
        """Test risk assessment."""
        config = ReviewConfig(
            tc_v1_path=Path("output/enhanced_tc/test_tc.md"),
            feature_id="FGR-TEST-001",
            sw_package="SVR26A",
            rapp_name="COM",
        )
        
        engine = ReviewEngine(config)
        
        # High score = Low risk
        risk, decision = engine._assess_risk(85)
        assert risk == "Low"
        assert decision == "Approve"
        
        # Medium score = Medium risk
        risk, decision = engine._assess_risk(65)
        assert risk == "Medium"
        assert decision == "Revise"
        
        # Low score = High risk
        risk, decision = engine._assess_risk(40)
        assert risk == "High"
        assert decision == "Regenerate"
    
    def test_detect_missing_scenarios(self):
        """Test missing scenario detection."""
        config = ReviewConfig(
            tc_v1_path=Path("output/enhanced_tc/test_tc.md"),
            feature_id="FGR-TEST-001",
            sw_package="SVR26A",
            rapp_name="COM",
        )
        
        engine = ReviewEngine(config)
        
        # Empty TC should have many missing scenarios
        tc_v1 = {"content": ""}
        missing = engine._detect_missing_scenarios(tc_v1, [])
        
        assert len(missing) > 0
        assert "Positive/Normal flow scenario" in missing or any("positive" in m.lower() for m in missing)
        
        # TC with some content
        tc_v1 = {"content": "This TC tests the normal flow and handles errors with boundary values"}
        missing = engine._detect_missing_scenarios(tc_v1, [])
        
        # Should have fewer missing scenarios
        assert len(missing) < 4


class TestCOMPlugin:
    """Test COM domain plugin."""
    
    def test_init(self):
        """Test COMPlugin initialization."""
        plugin = COMPlugin()
        
        assert plugin.rapp_name == "COM"
        assert len(plugin._rules) > 0
        assert len(plugin._scenarios) > 0
    
    def test_get_rules(self):
        """Test getting COM rules."""
        plugin = COMPlugin()
        rules = plugin.get_rules()
        
        assert len(rules) >= 9  # CP-1 to CP-9 plus specific rules
        
        # Check for specific rules
        rule_ids = [r.rule_id for r in rules]
        assert "CP-1" in rule_ids
        assert "CP-3" in rule_ids
        assert "CP-9" in rule_ids
    
    def test_get_scenarios(self):
        """Test getting COM scenarios."""
        plugin = COMPlugin()
        scenarios = plugin.get_scenarios()
        
        assert len(scenarios) >= 4  # At least 4 main scenarios
        
        # Check for specific scenarios
        scenario_ids = [s.scenario_id for s in scenarios]
        assert "COM-OS-1" in scenario_ids
        assert "COM-CH-1" in scenario_ids
        assert "COM-SW-1" in scenario_ids
    
    def test_validate_empty_tc(self):
        """Test validation with empty TC."""
        plugin = COMPlugin()
        
        result = plugin.validate("", {})
        
        assert result.rapp_name == "COM"
        assert len(result.findings) > 0
        assert len(result.missing_rules) > 0
        assert result.quality_adjustment < 0
    
    def test_validate_good_tc(self):
        """Test validation with good TC content."""
        plugin = COMPlugin()
        
        tc_content = """
        # Test Case: COM Overshooting Detection
        
        ## Test Overview
        This TC verifies COM overshooting detection with NE List scope.
        
        ## Precondition
        - NE List configured with Cell IDs
        - Detection Switch ON, Resolution Switch ON
        - CM/PM data collection enabled
        - Analytic Server connected
        
        ## Test Procedure
        1. Configure frequency f1=ON, f2=OFF
        2. Set optimization period to 30 minutes
        3. Verify TA far-distance ratio > 20%
        4. Check DL MAC Throughput < Th_DMacTputOp
        5. Verify Aggressor/Victim Cell identification
        
        ## Pass/Fail Criteria
        - CQI < 7 for Coverage Hole
        - BLER > 10%
        - Drop Rate > 2%
        """
        
        result = plugin.validate(tc_content, {})
        
        assert result.rapp_name == "COM"
        # Should have fewer missing rules
        assert len(result.missing_rules) < 10
        # Quality adjustment should be better than empty TC
        assert result.quality_adjustment > -20


class TestPluginManager:
    """Test PluginManager functionality."""
    
    def test_init(self):
        """Test PluginManager initialization."""
        manager = PluginManager()
        
        assert len(manager._plugins) == 0
    
    def test_register_plugin(self):
        """Test plugin registration."""
        manager = PluginManager()
        plugin = COMPlugin()
        
        manager.register_plugin(plugin)
        
        assert len(manager._plugins) == 1
        assert "COM" in manager._plugins
    
    def test_get_plugin(self):
        """Test getting plugin by name."""
        manager = PluginManager()
        plugin = COMPlugin()
        
        manager.register_plugin(plugin)
        
        retrieved = manager.get_plugin("COM")
        assert retrieved is not None
        assert retrieved.rapp_name == "COM"
        
        # Non-existent plugin
        retrieved = manager.get_plugin("NON_EXISTENT")
        assert retrieved is None
    
    def test_validate_with_plugin(self):
        """Test validation through plugin manager."""
        manager = PluginManager()
        plugin = COMPlugin()
        
        manager.register_plugin(plugin)
        
        tc_content = "Test TC with COM detection"
        result = manager.validate_with_plugin("COM", tc_content, {})
        
        assert result.rapp_name == "COM"
        assert hasattr(result, 'findings')
    
    def test_get_all_rapps(self):
        """Test getting all registered rAPPs."""
        manager = PluginManager()
        manager.register_plugin(COMPlugin())
        
        rapps = manager.get_all_rapps()
        
        assert "COM" in rapps
        assert len(rapps) == 1


class TestFinding:
    """Test Finding dataclass."""
    
    def test_create_finding(self):
        """Test creating a Finding."""
        finding = Finding(
            category="RC",
            check_id="RC-1",
            severity="High",
            description="Requirement not covered",
            tc_section="Test Procedure",
            evidence_status="Evidence-backed",
            human_review_required=False,
        )
        
        assert finding.category == "RC"
        assert finding.check_id == "RC-1"
        assert finding.severity == "High"
        assert finding.human_review_required is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
