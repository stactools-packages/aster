from stactools.testing import TestData

_external_data = {
    'AST_L1T_00305032000040446_20150409135350_78838.hdf': {
        'url':
        ('https://ai4epublictestdata.blob.core.windows.net/'
         'stactools/aster/AST_L1T_00305032000040446_20150409135350_78838.zip'),
        'compress':
        'zip'
    }
}

test_data = TestData(__file__, _external_data)
