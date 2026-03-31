print('Starting import test')
import sys
sys.path.insert(0, r'd:\bizMagnets-vite_haf\hariproject\Job_recommendation_web\backend')
print('Path added')
try:
    import app.main
    print('Import successful')
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()