import argparse


def get_option():
    """
    コマンドライン引数の解析
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", help="optional", action="store_true")
    args = parser.parse_args()
    return bool(args.fix)
