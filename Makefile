# Makefile for CryptoCore
.PHONY: build test clean help

# Variables
PYTHON := python3
PIP := pip3

# Colors
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m

help:
	@echo "$(GREEN)🚀 CryptoCore Build System$(NC)"
	@echo ""
	@echo "Available commands:"
	@echo "  $(YELLOW)make build$(NC) - Install dependencies"
	@echo "  $(YELLOW)make test$(NC)  - Run tests"
	@echo "  $(YELLOW)make clean$(NC) - Clean temporary files"
	@echo ""

build:
	@echo "$(YELLOW)📦 Installing dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Build completed!$(NC)"
	@echo ""
	@echo "$(GREEN)🎉 Usage examples:$(NC)"
	@echo "  $(PYTHON) cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input test.txt"
	@echo "  $(PYTHON) cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input final_encrypted.bin"

test:
	@echo "$(YELLOW)🧪 Running tests...$(NC)"
	@echo "$(YELLOW)Testing ECB mode...$(NC)"
	$(PYTHON) test_ecb_all.py
	@echo "$(YELLOW)Testing CLI...$(NC)"
	$(PYTHON) test_cli.py
	@echo "$(GREEN)✅ All tests completed!$(NC)"

clean:
	@echo "$(YELLOW)🧹 Cleaning temporary files...$(NC)"
	@rm -rf __pycache__
	@rm -rf cryptocore/__pycache__
	@rm -rf cryptocore/src/__pycache__
	@rm -rf cryptocore/src/modes/__pycache__
	@rm -rf tests/__pycache__
	@rm -f *.enc *.dec
	@echo "$(GREEN)✅ Clean completed!$(NC)"