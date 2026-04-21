from FunctionFlow.Fallback import fallback
from FunctionFlow.pause import pause
from FunctionFlow.repeat import repeat
from FunctionFlow.exitIF import exitFunctionIf
from FunctionFlow.skipTo import skipToFunction

try:
    print("FunctionFlow Initialized Successfully")
except Exception as e:
    print(f"Error occurred while initializing FunctionFlow: {e}")