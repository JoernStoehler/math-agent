# Priority Tasks for Math Agent System

## Current State Assessment

We've successfully:
- ✅ Removed unnecessary complexity (DI, lifespan managers)
- ✅ Kept status as simple strings
- ✅ Added basic error handling throughout

However, the system has **CRITICAL GAPS**:

## 🚨 Priority 1: Critical Path Testing

**The job executor is COMPLETELY UNTESTED** and marked with warnings. This is the core functionality!

### Task: Test Job Executor Core Functions
- Test command building for claude/gemini
- Test status updates work correctly
- Test error handling paths
- Test log streaming (mock the process)
- Skip PDF compilation tests (less critical)

**Why**: Without this, we can't trust the system will actually run jobs correctly.

## 🔴 Priority 2: Fix Test Environment

**All API tests are skipped** due to initialization issues.

### Task: Make Tests Actually Run
- Fix the test environment initialization
- Get basic API endpoint tests working
- Test at least: GET /, GET /jobs, GET /data/models
- Skip job creation tests until executor is tested

**Why**: Can't verify the API works without runnable tests.

## 📝 Priority 3: Basic Usage Documentation

**No clear documentation** on how to actually use the system.

### Task: Create Simple README
- How to start the server
- How to submit a job
- How to use the mock executor for demos
- What the system actually does

**Why**: Even simple code needs basic usage docs.

## 🔧 Priority 4: Verify Job Execution Flow

**The core flow is untested** end-to-end.

### Task: Manual Testing Guide
- Document how to manually test job creation
- Document expected behavior
- Create test data/exercises if missing

**Why**: Need to verify it actually works before automation.

## What We're NOT Doing

- ❌ 100% test coverage
- ❌ Complex integration tests
- ❌ Testing PDF compilation
- ❌ Performance optimization
- ❌ Advanced features

## Next Step

Start with **Priority 1** - testing the job executor's core functions. Without this, nothing else matters.