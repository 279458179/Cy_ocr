from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List
from paddleocr import PPStructureV3
import paddle


_PIPELINE = None


def _init_worker() -> None:
    """每个进程初始化一次推理管线与设备。"""
    global _PIPELINE
    device = "gpu" if paddle.device.is_compiled_with_cuda() and paddle.device.cuda.device_count() > 0 else "cpu"
    paddle.set_device(device)
    _PIPELINE = PPStructureV3(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False
    )


def _process_one(img_path_str: str, output_dir_str: str) -> str:
    """处理单张图片，返回图片文件名（无后缀）。"""
    global _PIPELINE
    img_path = Path(img_path_str)
    output_dir = Path(output_dir_str)
    output = _PIPELINE.predict(input=str(img_path))
    for res in output:
        res.print()
        save_subdir = output_dir / img_path.stem
        save_subdir.mkdir(exist_ok=True)
        res.save_to_json(save_path=str(save_subdir))
        res.save_to_markdown(save_path=str(save_subdir))
    return img_path.stem


if __name__ == "__main__":
    # 目录与输入收集
    input_dir = Path("images_input")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    img_exts = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    img_list: List[Path] = [
        p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in img_exts
    ]

    if not img_list:
        print("未发现可处理的图片文件。")
    else:
        max_workers = 4
        print(f"并发进程数: {max_workers}，待处理图片数: {len(img_list)}")
        with ProcessPoolExecutor(max_workers=max_workers, initializer=_init_worker) as executor:
            futures = [
                executor.submit(_process_one, str(p), str(output_dir)) for p in img_list
            ]
            for fut in as_completed(futures):
                try:
                    name = fut.result()
                    print(f"完成: {name}")
                except Exception as e:
                    print(f"处理失败: {e}")