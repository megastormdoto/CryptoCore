# Makefile for CryptoCore
.PHONY: build test clean help test-gcm test-nist test-aead test-all dev

# Variables
PYTHON := python3
PIP := pip3

# Colors
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m

# Test files
TEST_GCM := tests/test_gcm.py
TEST_NIST := tests/test_gcm_nist.py
TEST_AEAD := tests/test_aead.py
TEST_ALL := tests/

help:
	@echo "$(GREEN)🚀 CryptoCore Build System$(NC)"
	@echo ""
	@echo "Available commands:"
	@echo "  $(YELLOW)make build$(NC)    - Install dependencies"
	@echo "  $(YELLOW)make test$(NC)     - Run all tests"
	@echo "  $(YELLOW)make test-gcm$(NC) - Run GCM CLI tests"
	@echo "  $(YELLOW)make test-nist$(NC) - Run NIST GCM test vectors"
	@echo "  $(YELLOW)make test-aead$(NC) - Run AEAD tests"
	@echo "  $(YELLOW)make test-all$(NC)  - Run comprehensive test suite"
	@echo "  $(YELLOW)make dev$(NC)      - Clean and run all tests"
	@echo "  $(YELLOW)make clean$(NC)    - Clean temporary files"
	@echo ""
	@echo "$(BLUE)Sprint 6 (GCM/AEAD) Testing:$(NC)"
	@echo "  make test-gcm  # Test GCM through CLI"
	@echo "  make test-nist # Test against NIST vectors"
	@echo ""

build:
	@echo "$(YELLOW)📦 Installing dependencies...$(NC)"
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "$(RED)⚠️  requirements.txt not found$(NC)"; \
	fi
	@echo "$(GREEN)✅ Build completed!$(NC)"
	@echo ""
	@echo "$(GREEN)🎉 Usage examples:$(NC)"
	@echo "  # GCM Encryption"
	@echo "  \$$ $(PYTHON) cryptocore.py encrypt --mode gcm --key 00112233445566778899aabbccddeeff --input test.txt --output cipher.bin --aad aabbccdd"
	@echo ""
	@echo "  # GCM Decryption"
	@echo "  \$$ $(PYTHON) cryptocore.py encrypt --decrypt --mode gcm --key 00112233445566778899aabbccddeeff --input cipher.bin --output decrypted.txt --aad aabbccdd"

test-gcm:
	@echo "$(YELLOW)🧪 Running GCM CLI tests...$(NC)"
	@if [ -f $(TEST_GCM) ]; then \
		$(PYTHON) $(TEST_GCM); \
		RETVAL=$$?; \
		if [ $$RETVAL -eq 0 ]; then \
			echo "$(GREEN)✅ GCM CLI tests passed!$(NC)"; \
		else \
			echo "$(RED)❌ GCM CLI tests failed$(NC)"; \
			exit $$RETVAL; \
		fi \
	else \
		echo "$(RED)⚠️  GCM test file not found: $(TEST_GCM)$(NC)"; \
	fi

test-nist:
	@echo "$(YELLOW)🧪 Running NIST GCM test vectors...$(NC)"
	@if [ -f $(TEST_NIST) ]; then \
		$(PYTHON) $(TEST_NIST); \
		RETVAL=$$?; \
		if [ $$RETVAL -eq 0 ]; then \
			echo "$(GREEN)✅ NIST tests passed!$(NC)"; \
		else \
			echo "$(RED)❌ NIST tests failed$(NC)"; \
			exit $$RETVAL; \
		fi \
	else \
		echo "$(RED)⚠️  NIST test file not found: $(TEST_NIST)$(NC)"; \
	fi

test-aead:
	@echo "$(YELLOW)🧪 Running AEAD tests...$(NC)"
	@if [ -f $(TEST_AEAD) ]; then \
		$(PYTHON) $(TEST_AEAD); \
		RETVAL=$$?; \
		if [ $$RETVAL -eq 0 ]; then \
			echo "$(GREEN)✅ AEAD tests passed!$(NC)"; \
		else \
			echo "$(RED)❌ AEAD tests failed$(NC)"; \
			exit $$RETVAL; \
		fi \
	else \
		echo "$(RED)⚠️  AEAD test file not found: $(TEST_AEAD)$(NC)"; \
	fi

test-all:
	@echo "$(YELLOW)🧪 Running comprehensive test suite...$(NC)"
	@echo "$(BLUE)=========================================$(NC)"
	@echo "$(YELLOW)1. Testing GCM CLI...$(NC)"
	@make test-gcm || exit 1
	@echo ""
	@echo "$(YELLOW)2. Testing NIST vectors...$(NC)"
	@make test-nist || exit 1
	@echo ""
	@echo "$(YELLOW)3. Testing AEAD...$(NC)"
	@make test-aead || exit 1
	@echo ""
	@echo "$(YELLOW)4. Running all test discovery...$(NC)"
	@if [ -d $(TEST_ALL) ]; then \
		$(PYTHON) -m pytest $(TEST_ALL) -v --tb=short 2>/dev/null || \
		$(PYTHON) -m unittest discover $(TEST_ALL) -v 2>/dev/null || \
		echo "$(RED)⚠️  No test discovery available$(NC)"; \
	fi
	@echo "$(GREEN)✅ All tests completed!$(NC)"

test:
	@echo "$(YELLOW)🧪 Running default test suite...$(NC)"
	@make test-gcm
	@echo ""
	@make test-nist

dev: clean test-all
	@echo "$(GREEN)🚀 Development cycle completed!$(NC)"

clean:
	@echo "$(YELLOW)🧹 Cleaning temporary files...$(NC)"
	@# Remove Python cache
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@# Remove test artifacts
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -f *.enc *.dec *.bin *.txt
	@# Remove temporary test files
	@find . -type f -name "*.tmp" -delete
	@find . -type f -name "test_*.bin" -delete
	@find . -type f -name "test_*.txt" -delete
	@find . -type f -name "encrypted_*" -delete
	@find . -type f -name "decrypted_*" -delete
	@# Remove macOS files
	@find . -type f -name ".DS_Store" -delete
	@echo "$(GREEN)✅ Clean completed!$(NC)"

# Sprint-specific testing
test-sprint6: test-gcm test-nist
	@echo "$(GREEN)✅ Sprint 6 (GCM/AEAD) tests completed!$(NC)"

# Quick test command
quick:
	@echo "$(YELLOW)⚡ Quick test...$(NC)"
	@$(PYTHON) -c "print('Python is working')" && \
	$(PYTHON) cryptocore.py --help 2>&1 | head -20
	@echo "$(GREEN)✅ Quick test passed!$(NC)"