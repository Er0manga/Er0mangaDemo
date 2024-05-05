import gradio as gr


import os
import sys
base_path = os.path.expanduser('~')

sys.path.append(os.path.join(base_path, 'Er0mangaSeg/'))
sys.path.append(os.path.join(base_path, 'Er0mangaSeg/demo'))
from image_demo_tta import init_seg_model, inference_tta

sys.path.append(os.path.join(base_path, 'Er0mangaInpaint/'))
sys.path.append(os.path.join(base_path, 'Er0mangaInpaint/bin'))
from uncen import init_inpaint_model, inpaint


import time
import numpy as np
import cv2
import shutil
import torch


if torch.cuda.is_available():
    print('GPU found!')
    device = 'cuda:0'
else:
    print('GPU not found! Using CPU')
    device = 'cpu'

 
config = os.path.join(base_path, 'Er0mangaSeg/configs/convnext/convnext_h.py')
checkpoint = os.path.join(base_path, 'Er0mangaSeg/pretrained/convnext_1024_iter_400.pth')
model_seg = init_seg_model(config, checkpoint, device=device)
print('Segmentation initialized')


inp_model_path = os.path.join(base_path, 'Er0mangaInpaint/pretrained/00-30-09')
model_inp = init_inpaint_model(inp_model_path)
print('Inpainting initialized')


def proc(input_img):

    try:

        s = time.time()

        out_mask, raw_mask = inference_tta(model_seg, input_img)
        out_mask = np.dstack([out_mask, out_mask, out_mask])
        raw_mask = np.dstack([raw_mask, raw_mask, raw_mask])

        output_img, out_dbg = inpaint(model_inp, input_img, out_mask)

        e = time.time()
        print(f"proc_time: {e-s:.2f}")

        return output_img#, raw_mask

    except Exception as e:
        raise gr.Error(e)


def proc_batch(batch):

    res = []
    try:

        s = time.time()

        out_p = os.path.dirname(batch[0][0])
        salt = str(np.random.randint(1e10))
        out_p_d = os.path.join(out_p, '__salt_img__'+salt)
        out_p_m = os.path.join(out_p, '__salt_mask__'+salt)
        os.mkdir(out_p_d)
        os.mkdir(out_p_m)

        for i in range(len(batch)):
            input_path = batch[i][0]
            inp_name = os.path.basename(input_path)
            input_img = cv2.cvtColor(cv2.imread(input_path), cv2.COLOR_BGR2RGB)

            out_mask, raw_mask = inference_tta(model_seg, input_img)
            out_mask = np.dstack([out_mask, out_mask, out_mask])
            raw_mask = np.dstack([raw_mask, raw_mask, raw_mask])

            output_img, out_dbg = inpaint(model_inp, input_img, out_mask)
            out_path_img = os.path.join(out_p_d, inp_name)
            out_path_mask = os.path.join(out_p_m, inp_name+'.png')
            cv2.imwrite(out_path_img, cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
            cv2.imwrite(out_path_mask, raw_mask)
            res.append(out_path_img)

        ar_path = os.path.join(out_p, 'output')
        shutil.make_archive(ar_path, 'zip', out_p_d)

        ar_path_m = os.path.join(out_p, 'output_mask')
        shutil.make_archive(ar_path_m, 'zip', out_p_m)

        e = time.time()
        print(f"batch proc_time: {e-s:.2f}")

        return res, ar_path + '.zip', ar_path_m + '.zip'

    except Exception as e:
        raise gr.Error(e)



demo1 = gr.Interface(proc, gr.Image(), gr.Image(format='png'), delete_cache=(7200, 7200), allow_flagging='never')
demo2 = gr.Interface(proc_batch, gr.Gallery(), [gr.Gallery(value='str', format='png'), gr.File(), gr.File()], delete_cache=(7200, 7200), allow_flagging='never')
demo = gr.TabbedInterface([demo1, demo2], ["Single image processing", "Batch processing (experimental)"])

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0', server_port=7860)


