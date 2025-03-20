from pptx2md import convert

TEXT_PPTX_PATH = '../test_ppt/demo.pptx'

def pptx_convert(pptx_path, output_path):
    convert(
        pptx_path=pptx_path,
        output=output_path
    )


if __name__ == '__main__':
    pptx_convert(TEXT_PPTX_PATH, 'test.md')