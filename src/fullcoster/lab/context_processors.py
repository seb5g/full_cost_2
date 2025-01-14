from pathlib import Path
import importlib
all_activity_short = []
all_activity_long = []
base = Path(__file__).parent.parent
dirs = []
for dir_tmp in base.iterdir():
    if dir_tmp.is_dir():
        if dir_tmp.joinpath('views.py').exists():
            if dir_tmp.parts[-1] != 'lab':
                dirs.append(dir_tmp)


for p in dirs:
    all_activity_short.append(p.parts[-1])
    mod = importlib.import_module(f'{all_activity_short[-1]}.views')
    all_activity_long.append(getattr(mod,'activity_long'))



def get_all_activity(request):
    return {'test_act': ['test1', 'test2', 'test3'], 'all_activity_short': all_activity_short, 'all_activity_long': all_activity_long,}
