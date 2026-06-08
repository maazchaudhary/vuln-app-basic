---

name: security-audit-report
description: Perform a comprehensive application security assessment of a repository and generate a consulting-grade PDF security audit report. Analyze source code, architecture, configuration, dependencies, authentication, authorization, APIs, cryptography, secrets management, logging, monitoring, and deployment security. Use OWASP ASVS, OWASP Top 10, CWE, CVSS v3.1, and NIST SSDF to identify vulnerabilities, assign risk ratings, evaluate security maturity, and produce SECURITY_AUDIT_REPORT.pdf suitable for engineering, management, clients, instructors, and auditors.

--------

# Security Audit Report

## Purpose

Perform a comprehensive security assessment of an entire codebase and generate a professional security audit report.

Act as a Senior Application Security Consultant delivering a consulting-grade security review.

The primary deliverable is:

**SECURITY_AUDIT_REPORT.pdf**

---

# When To Use

Use this skill when:

- Auditing a software project
- Reviewing source code security
- Performing secure code reviews
- Conducting architecture security assessments
- Evaluating applications against OWASP standards
- Assessing APIs for security weaknesses
- Reviewing authentication and authorization controls
- Generating client-facing security reports
- Producing instructor-grade assessment reports
- Evaluating security maturity
- Preparing compliance and audit documentation

---

# Invocation Examples

Examples:

- Audit this repository and generate a security report.
- Perform a complete application security assessment.
- Review this codebase using OWASP ASVS.
- Conduct a secure code review.
- Analyze this repository and generate a PDF security audit report.
- Evaluate the security posture of this application.
- Produce a consulting-grade security assessment.

---

# Security Standards

Base all assessments on:

## OWASP ASVS

Latest available version.

Use ASVS requirements to evaluate:

- Architecture
- Authentication
- Session Management
- Access Control
- Validation
- API Security
- Cryptography
- Logging
- Configuration

---

## OWASP Top 10

Map findings to applicable categories.

Examples:

- A01 Broken Access Control
- A02 Cryptographic Failures
- A03 Injection
- A04 Insecure Design
- A05 Security Misconfiguration
- A06 Vulnerable Components
- A07 Identification and Authentication Failures
- A08 Software and Data Integrity Failures
- A09 Security Logging and Monitoring Failures
- A10 Server-Side Request Forgery

---

## CWE

Map every finding to one or more CWE identifiers.

Examples:

- CWE-79
- CWE-89
- CWE-287
- CWE-352
- CWE-639
- CWE-798

---

## CVSS v3.1

Assign CVSS scores to every finding.

Include:

- Severity
- Base Score
- Vector String

---

## NIST SSDF

Evaluate security maturity using:

- PO — Prepare the Organization
- PS — Protect the Software
- PW — Produce Well-Secured Software
- RV — Respond to Vulnerabilities

---

# Assessment Scope

Analyze the entire repository.

Do not limit analysis to a subset of files.

Review:

## Source Code

- Backend code
- Frontend code
- Mobile code
- Desktop code
- Serverless code
- Infrastructure code
- Shared libraries

---

## Application Architecture

Evaluate:

- Trust boundaries
- Data flow
- Security controls
- Authentication design
- Authorization design
- Network exposure
- Service interactions

---

## Authentication

Review:

- Login mechanisms
- Password handling
- Password storage
- Password reset functionality
- MFA support
- Account recovery
- Credential lifecycle

---

## Authorization

Review:

- RBAC
- ABAC
- Access checks
- Privilege escalation risks
- Horizontal privilege escalation
- Vertical privilege escalation
- Multi-tenant isolation

---

## Session Management

Review:

- Session creation
- Session storage
- Session expiration
- Session revocation
- JWT validation
- Refresh token security

---

## Input Validation

Review:

- User input handling
- Validation controls
- Sanitization controls
- Data processing workflows

Check for:

- SQL Injection
- NoSQL Injection
- LDAP Injection
- Command Injection
- Path Traversal
- XSS
- SSTI
- Deserialization flaws

---

## API Security

Review:

- Authentication
- Authorization
- Object-level access control
- Function-level access control
- Rate limiting
- Data exposure
- Input validation
- API abuse protections

---

## Cryptography

Review:

- Encryption algorithms
- Hashing algorithms
- Key management
- Secret storage
- Random number generation
- Certificate validation

---

## Secrets Management

Review:

- Hardcoded credentials
- API keys
- Tokens
- Secrets in repositories
- Secrets in configuration files
- Secrets in CI/CD pipelines

---

## Dependency Security

Review:

- Vulnerable dependencies
- Outdated dependencies
- Supply chain risks
- Package integrity concerns

---

## Logging And Monitoring

Review:

- Audit logging
- Security events
- Alerting
- Incident visibility
- Monitoring coverage

---

## Configuration Security

Review:

- Application configuration
- Environment configuration
- Framework configuration
- Container configuration
- Infrastructure configuration

---

## Deployment Security

Review:

- CI/CD pipelines
- Container deployments
- Cloud deployments
- Infrastructure-as-Code
- Runtime hardening

---

# Assessment Workflow

Follow this workflow.

---

## Phase 1 — Repository Discovery

Identify:

- Languages
- Frameworks
- Dependencies
- APIs
- Services
- Databases
- Authentication mechanisms
- Deployment architecture
- Security controls

Document architecture observations.

---

## Phase 2 — Security Analysis

Perform a deep security review.

Identify:

- Vulnerabilities
- Misconfigurations
- Weak security controls
- Insecure coding patterns
- Architectural weaknesses
- Operational risks

Do not rely solely on automated findings.

Perform reasoning-based analysis.

---

## Phase 3 — Finding Validation

Validate findings.

Avoid false positives.

Confirm:

- Vulnerability existence
- Affected components
- Exploitation feasibility
- Business impact

---

## Phase 4 — Risk Assessment

Assign:

- Severity
- CVSS score
- CWE mappings
- OWASP mappings

Determine remediation priority.

---

## Phase 5 — Security Maturity Assessment

Evaluate:

- Architecture maturity
- Development maturity
- Security process maturity
- Secure deployment maturity

Generate maturity observations.

---

# Finding Requirements

Every finding must contain the following sections.

---

## Finding ID

Format:

SEC-001

SEC-002

SEC-003

---

## Title

Clear concise title.

Example:

Broken Object Level Authorization

---

## Severity

One of:

- Critical
- High
- Medium
- Low
- Informational

---

## CVSS

Include:

### Score

Example:

8.8 High

### Vector

Example:

AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H

---

## CWE Mapping

Example:

CWE-639

Authorization Bypass Through User-Controlled Key

---

## OWASP Mapping

Example:

OWASP Top 10

A01 Broken Access Control

OWASP ASVS

V4 Access Control

---

## Location

Provide:

- File path
- Function
- Class
- Endpoint
- Service

When available.

---

## Description

Explain the issue.

---

## Technical Details

Provide technical analysis.

Explain:

- Root cause
- Vulnerable behavior
- Security implications

---

## Evidence

Provide supporting evidence.

Examples:

- Code snippets
- Configurations
- Requests
- Responses
- Logs

Evidence must directly support the finding.

---

## Impact

Explain:

### Confidentiality Impact

### Integrity Impact

### Availability Impact

### Business Impact

---

## Exploitation Scenario

Describe:

- Attacker requirements
- Attack steps
- Likely outcome

Use realistic scenarios.

---

## Remediation

Provide actionable guidance.

Recommendations must be implementation-focused.

Avoid generic advice.

---

## Secure Code Example

Provide corrected code.

Use the repository language when possible.

Show secure implementation.

---

# Security Score

Generate an overall score.

Range:

0–100

Consider:

- Critical findings
- High findings
- Medium findings
- Security control coverage
- Architecture maturity
- Operational maturity

Provide:

## Score

Example:

82 / 100

## Grade

| Score | Grade |
|---------|---------|
| 90-100 | A |
| 80-89 | B |
| 70-79 | C |
| 60-69 | D |
| Below 60 | F |

Provide rationale.

---

# OWASP ASVS Assessment

Generate an ASVS assessment table.

| Category | Status | Notes |
|-----------|-----------|-----------|
| Architecture | Pass / Partial / Fail | Notes |
| Authentication | Pass / Partial / Fail | Notes |
| Session Management | Pass / Partial / Fail | Notes |
| Access Control | Pass / Partial / Fail | Notes |
| Validation | Pass / Partial / Fail | Notes |
| Cryptography | Pass / Partial / Fail | Notes |
| Logging | Pass / Partial / Fail | Notes |
| API Security | Pass / Partial / Fail | Notes |
| Configuration | Pass / Partial / Fail | Notes |

Provide maturity observations.

---

# Risk Matrix

Generate a risk matrix.

Likelihood:

- Low
- Medium
- High

Impact:

- Low
- Medium
- High

Include all findings.

---

# Remediation Roadmap

Create a prioritized remediation plan.

## Immediate (0–30 Days)

Focus:

- Critical findings
- High findings

---

## Short-Term (30–90 Days)

Focus:

- Medium findings
- Security control improvements

---

## Long-Term (90+ Days)

Focus:

- Architecture improvements
- Security maturity initiatives
- Process improvements

---

# NIST SSDF Assessment

Evaluate:

## PO — Prepare the Organization

## PS — Protect the Software

## PW — Produce Well-Secured Software

## RV — Respond to Vulnerabilities

Provide:

- Current maturity
- Gaps
- Recommendations

---

# Executive Summary

Write for executives and management.

Include:

- Overall security posture
- Key strengths
- Major risks
- Critical findings
- Recommended next actions

Avoid excessive technical detail.

---

# Final Security Rating

Provide:

## Overall Rating

Examples:

- Excellent
- Good
- Fair
- Poor
- Critical Risk

---

## Risk Level

Examples:

- Low
- Moderate
- High
- Critical

---

## Security Maturity

Examples:

- Initial
- Developing
- Intermediate
- Advanced
- Mature

Provide concise justification.

---

# PDF Generation Requirements

Generate:

SECURITY_AUDIT_REPORT.pdf

The PDF must include:

1. Cover Page
2. Table of Contents
3. Executive Summary
4. Security Score
5. OWASP ASVS Assessment
6. Findings
7. Risk Matrix
8. Remediation Roadmap
9. NIST SSDF Assessment
10. Final Security Rating

Formatting requirements:

- Professional consulting style
- Consistent typography
- Section hierarchy
- Page numbers
- Readable tables
- Readable code snippets
- Executive-ready presentation quality

---

# Output Requirements

Primary Deliverable:

SECURITY_AUDIT_REPORT.pdf

Additional Outputs:

- Executive Summary
- Findings Summary
- Security Score
- Risk Matrix
- Remediation Roadmap
- Final Security Rating

Prioritize:

- Accuracy
- Evidence-based findings
- Actionable remediation
- Practical security improvements
- Clear risk communication

Never suppress findings because remediation is difficult.

Always support findings with evidence whenever available.
```
