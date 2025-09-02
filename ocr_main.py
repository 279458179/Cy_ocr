from pathlib import Path
from paddleocr import PPStructureV3

pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

# 处理 images_input 目录下所有图片
input_dir = Path("images_input")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# 支持的图片格式
img_exts = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

for img_path in input_dir.iterdir():
    if img_path.suffix.lower() in img_exts:
        output = pipeline.predict(input=str(img_path))
        for res in output:
            res.print()
            # 以图片名为子目录保存结果
            save_subdir = output_dir / img_path.stem
            save_subdir.mkdir(exist_ok=True)
            res.save_to_json(save_path=str(save_subdir))
            res.save_to_markdown(save_path=str(save_subdir))