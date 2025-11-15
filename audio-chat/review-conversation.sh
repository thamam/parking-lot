#!/bin/bash
# Conversation Review Voice Agent CLI Wrapper
# Provides convenient shortcuts for running the agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_SCRIPT="$SCRIPT_DIR/src/conversation_review_agent.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print usage
usage() {
    cat << EOF
Conversation Review Voice Agent - CLI Wrapper

Usage:
  $(basename "$0") [OPTIONS] <conversation_file>

Options:
  -i, --interactive     Run in interactive mode (gather decisions)
  -h, --help           Show this help message
  -v, --version        Show version information
  -t, --test           Run with example conversation

Examples:
  # Analyze a conversation (non-interactive)
  $(basename "$0") conversation.json

  # Interactive session
  $(basename "$0") -i conversation.json

  # Test with example
  $(basename "$0") -t simple

Available test conversations:
  - simple    Basic example with 4 questions
  - complex   Advanced example with 8 questions (mixed priority)
  - text      Plain text format example

Environment:
  PYTHON_BIN   Python executable to use (default: python3)

Output:
  Analysis results are displayed on screen and saved to ./output/
  - summary_TIMESTAMP.xml  (Structured XML)
  - summary_TIMESTAMP.json (JSON format)
  - summary_TIMESTAMP.md   (Human-readable Markdown)

EOF
    exit 0
}

# Print version
version() {
    echo "Conversation Review Voice Agent v1.0.0"
    exit 0
}

# Check if Python is available
check_python() {
    PYTHON_BIN="${PYTHON_BIN:-python3}"

    if ! command -v "$PYTHON_BIN" &> /dev/null; then
        echo -e "${RED}Error: Python 3 not found${NC}"
        echo "Please install Python 3.8+ or set PYTHON_BIN environment variable"
        exit 1
    fi

    # Check Python version
    version=$("$PYTHON_BIN" --version 2>&1 | awk '{print $2}')
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)

    if [ "$major" -lt 3 ] || { [ "$major" -eq 3 ] && [ "$minor" -lt 8 ]; }; then
        echo -e "${RED}Error: Python 3.8+ required, found $version${NC}"
        exit 1
    fi
}

# Main execution
main() {
    local interactive=""
    local conversation_file=""
    local test_mode=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--interactive)
                interactive="--interactive"
                shift
                ;;
            -h|--help)
                usage
                ;;
            -v|--version)
                version
                ;;
            -t|--test)
                test_mode="$2"
                shift 2
                ;;
            -*)
                echo -e "${RED}Error: Unknown option $1${NC}"
                echo "Use -h for help"
                exit 1
                ;;
            *)
                conversation_file="$1"
                shift
                ;;
        esac
    done

    check_python

    # Handle test mode
    if [ -n "$test_mode" ]; then
        case "$test_mode" in
            simple)
                conversation_file="$SCRIPT_DIR/examples/example_conversation_simple.json"
                ;;
            complex)
                conversation_file="$SCRIPT_DIR/examples/example_conversation_complex.json"
                ;;
            text)
                conversation_file="$SCRIPT_DIR/examples/example_conversation_text.txt"
                ;;
            *)
                echo -e "${RED}Error: Unknown test conversation '$test_mode'${NC}"
                echo "Available: simple, complex, text"
                exit 1
                ;;
        esac
        echo -e "${YELLOW}Running test with: $test_mode${NC}"
    fi

    # Check if conversation file is provided
    if [ -z "$conversation_file" ]; then
        echo -e "${RED}Error: No conversation file specified${NC}"
        echo "Use -h for help"
        exit 1
    fi

    # Check if file exists
    if [ ! -f "$conversation_file" ]; then
        echo -e "${RED}Error: File not found: $conversation_file${NC}"
        exit 1
    fi

    # Run the agent
    echo -e "${GREEN}Starting Conversation Review Agent...${NC}"
    echo ""

    "$PYTHON_BIN" "$AGENT_SCRIPT" $interactive "$conversation_file"

    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Session completed successfully${NC}"
    else
        echo ""
        echo -e "${RED}✗ Session failed with exit code $exit_code${NC}"
    fi

    exit $exit_code
}

main "$@"
