from FunctionFlow.Fallback import fallback
from FunctionFlow.pause import pause
from FunctionFlow.repeat import repeat
from FunctionFlow.repeat_until import repeat_until
from FunctionFlow.exitIF import exitFunctionIf
from FunctionFlow.skipTo import skipToFunction
from FunctionFlow.sleep import sleep, is_paused, pause_sleep, unpause
from FunctionFlow.runList import run_list

try:
    print("FunctionFlow Initialized Successfully")
except Exception as e:
    print(f"Error occurred while initializing FunctionFlow: {e}")
