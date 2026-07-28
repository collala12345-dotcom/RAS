\## 📦 Phase 1: Evidence Collection



\### 수행 Block (1-1 \~ 1-9) - \*\*반드시 순서대로 수행\*\*

| Block | 내용 | Python 함수 |

|-------|------|-------------|

| 1-1 | TC Intake \& Intent Understanding | `extract\_search\_keywords()` |

**TC 의도 파악**	TC v1 이 무엇을 검증하려는지 이해해야 올바른 검색어를 추출할 수 있음



| 1-2 | Requirement Matching | FR 매핑 |

**요구사항 매핑**	FR 요구사항과 TC 검증 항목을 1:1 대응시켜 누락 확인



| 1-3 | Design Behavior Retrieval | BM25 검색 |

**동작 원리 검색**	HLD/DLD 설계 문서에서 시스템 동작 방식 검색



| 1-4 | Algorithm/KPI/Parameter Retrieval | BM25 검색 |

**알고리즘/수치 검색**	알고리즘 로직, KPI 임계값, 파라미터 정의 검색



| 1-5 | Standard/3GPP Retrieval | BM25 검색 |

**표준/3GPP 검색**	3GPP 표준 문서에서 관련 정의와 측정 방법 검색



| 1-6 | Legacy TC Retrieval | BM25 검색 |

**기존 TC 검색**	유사한 기존 Test Case 패턴 검색



| 1-7 | Issue/Bug/Test Result Retrieval | BM25 검색 |

**이슈/버그 검색**	과거 현장 문제, 상용 장애, Bug 리포트 검색



| 1-8 | Cross-rAPP/Common Pattern Retrieval | BM25 검색 |

**교차 rAPP 검색**	다른 rAPP 과의 연동 패턴, 공통 검증 관점 검색



| 1-9 | Evidence Grading \& Pack Generation | `grade\_evidence\_by\_bm25\_score()` |

**근거 등급화	BM25 점수로 Strong/Supporting/Weak 등급 부여 및 Pack 생성**



\### Gate 1 판정 (명시적 기준)

\- `READY`: Strong evidence ≥ 1 개 → Phase 2 전체 검토

\- `READY\_WITH\_GAPS`: Strong 0 개 but Supporting ≥ 1 개 → Phase 2 수행 (근거 제한)

\- `BLOCKED`: Evidence 0 개 → \*\*Human Review 로 이관 (Phase 2 진행 금지)\*\*





\## 📝 Phase 2: Review Queue 생성



\### 수행 Block (2-1 \~ 2-10) - \*\*반드시 순서대로 수행\*\*

| Block | 내용 | Python 함수 |

|-------|------|-------------|

| 2-1 | Requirement Coverage (Intent/Action/Oracle Link) | `\_run\_block\_2\_1\_requirement\_coverage()` |

**요구사항 충족도 검토**	TC 의 Purpose-Procedure-Pass/Fail 이 FR 요구사항과 연결되는지 확인



| 2-2 | Scope/Precondition Review | `\_run\_block\_2\_2\_scope\_precondition()` |

**범위/사전조건 검토**	TC 의 전제조건이 명확한지, NE List/설정 값 등 누락 확인



| 2-3 | Procedure Executability Review | `\_run\_block\_2\_3\_procedure\_executability()` |

**절차 실행 가능성 검토**	TC 절차가 실제로 실행 가능한 API/명령어인지 확인



| 2-4 | Observability \& Pass/Fail Review | `\_run\_block\_2\_4\_observability\_passfail()` |

**관측 가능성/판정기준 검토**	PM/CM 데이터 수집 가능 여부, Pass/Fail 기준 명확성 확인



| 2-5 | Scenario Coverage Review | `\_run\_block\_2\_5\_scenario\_coverage()` |

**시나리오 충족도 검토**	Normal 뿐 아니라 Negative/Abnormal 시나리오 포함 여부 확인



| 2-6 | Historical Risk \& Consistency Review | `\_run\_block\_2\_6\_historical\_consistency()` |

**과거 위험/일관성 검토**	과거 이슈/장애 사례와 TC 일관성 확인



| 2-7 | Gotcha Checkpoint 적용 | `\_run\_block\_2\_7\_gotcha\_checkpoint()` |

**Gotcha Checkpoint 적용**	과거 실수 (Gotcha) 를 Checkpoint 로 변환하여 재발 방지



| 2-8 | Atomic Change Proposal Generation | `\_generate\_change\_proposals()` |

**원자적 변경 제안 생성**	각 변경 사항을 독립적으로 검토 가능하도록 분리



| 2-9 | Priority \& Evidence Status (P1/P2/P3, 한글 근거) | `\_assign\_priority()` |

**우선순위/근거 상태 부여	P1/P2/P3 우선순위와 근거 상태 (한글) 부여**



| 2-10 | Review Queue Generation | `ReviewQueue()` 생성 |

**Review Queue 생성**	Reviewer 검토를 위한 변경 제안서 생성







\## 🛠️ Phase 3: Controlled Merge



\### 수행 Block (3-1 \~ 3-7) - \*\*반드시 순서대로 수행\*\*

| Block | 내용 | Python 함수 |

|-------|------|-------------|

| 3-1 | Reviewer Decision Parser | `\_parse\_reviewer\_decision()` |

**Reviewer 결정 파싱**	Reviewer 가 입력한 승인/거절 결정을 해석



| 3-2 | Decision Validation | `\_validate\_decision()` |

**결정 검증**	결정의 유효성 (중복, 누락) 확인



| 3-3 | Approved Change Classification | `\_classify\_approved\_changes()` |

**승인된 변경 분류**	승인된 변경만 분류하여 병합 대상 선정



| 3-4 | Controlled Merge (ADD/MODIFY/DELETE/SPLIT) | `\_apply\_change()` |

**통제된 병합**	 ADD/MODIFY/DELETE/SPLIT 연산으로 TC v1 에 병합



| 3-5 | TC v2 Generation \& Integrity Check | `\_verify\_tc\_v2()` |

**TC v2 생성/무결성 검증**	TC v2 생성 후 구조적 완전성 확인



| 3-6 | Change History Generation | `\_generate\_change\_history()` |

**변경 이력 생성**	어떤 변경이 승인되어 반영되었는지 이력 기록



| 3-7 | Final Output Packaging | `\_package\_output()` |

**최종 출력 패키징**	output/ 폴더에 TC v2 와 변경 이력 파일 생성



\### Gate 3: Decision Readiness Gate

\- G3-01: Review ID 와 Proposal Version 일치

\- G3-02: TC v1 checksum 일치

\- G3-03: 모든 Change ID 존재

\- G3-04: 결정 중복 없음

\- G3-05: WAITING 항목 없음

\- G3-06: 수정후승인 항목에 최종 반영 내용 있음

