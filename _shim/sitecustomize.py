import sys
class _Block:
    def find_module(self, name, path=None):
        return self if name == 'pptx' or name.startswith('pptx' + '.') else None
    def load_module(self, name):
        raise ImportError(name)
    def find_spec(self, name, path=None, target=None):
        if name == 'pptx' or name.startswith('pptx' + '.'):
            raise ImportError(name)
        return None
sys.meta_path.insert(0, _Block())
