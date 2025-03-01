'''测试脚本（视频处理）'''
# test.py
from spatial_network import build_SpatialNet
from temporal_network import build_TemporalNet
from smooth_network import build_SmoothNet
from utils.torch_tps_transform import transformer as tps_transform
# 假设 get_rigid_mesh, get_norm_mesh, recover_mesh, get_stable_sqe 已定义或需导入

def process_frame_pair(frame1, frame2, spatial_net, temporal_net, smooth_net, buffer):
    # 初始化缓冲区
    if not buffer['initialized']:
        buffer['img1_list'] = []
        buffer['img2_list'] = []
        buffer['smotion1_list'] = []
        buffer['smotion2_list'] = []
        buffer['tmotion1_list'] = []
        buffer['tmotion2_list'] = []
        buffer['smesh1_list'] = []
        buffer['smesh2_list'] = []
        buffer['tsmotion1_list'] = []
        buffer['tsmotion2_list'] = []
        buffer['smooth_mesh1'] = None
        buffer['smooth_mesh2'] = None
        buffer['idx'] = 0
        buffer['initialized'] = True

    # 添加当前帧
    buffer['img1_list'].append(frame1.cuda())
    buffer['img2_list'].append(frame2.cuda())

    # 空间对齐
    with torch.no_grad():
        spatial_out = build_SpatialNet(spatial_net, frame1.cuda(), frame2.cuda())
    buffer['smotion1_list'].append(spatial_out['motion1'])
    buffer['smotion2_list'].append(spatial_out['motion2'])

    # 时间对齐
    if len(buffer['img1_list']) >= 2:
        with torch.no_grad():
            temporal_out1 = build_TemporalNet(temporal_net, buffer['img1_list'])
            temporal_out2 = build_TemporalNet(temporal_net, buffer['img2_list'])
        buffer['tmotion1_list'] = temporal_out1['motion_list']
        buffer['tmotion2_list'] = temporal_out2['motion_list']

    # 计算 tsmotion
    rigid_mesh = get_rigid_mesh(1, 360, 480)
    if len(buffer['tmotion1_list']) > 0:
        for k in range(len(buffer['tmotion1_list'])):
            smesh1 = rigid_mesh + buffer['smotion1_list'][k]
            smesh2 = rigid_mesh + buffer['smotion2_list'][k]
            tsmotion1 = torch.zeros_like(smesh1) if k == 0 else recover_mesh(
                tps_transform_point.transformer(
                    get_norm_mesh(rigid_mesh + buffer['tmotion1_list'][k], 360, 480),
                    get_norm_mesh(rigid_mesh, 360, 480),
                    get_norm_mesh(rigid_mesh + buffer['smotion1_list'][k-1], 360, 480)
                ), 360, 480) - smesh1
            tsmotion2 = torch.zeros_like(smesh2) if k == 0 else recover_mesh(
                tps_transform_point.transformer(
                    get_norm_mesh(rigid_mesh + buffer['tmotion2_list'][k], 360, 480),
                    get_norm_mesh(rigid_mesh, 360, 480),
                    get_norm_mesh(rigid_mesh + buffer['smotion2_list'][k-1], 360, 480)
                ), 360, 480) - smesh2
            buffer['smesh1_list'].append(smesh1)
            buffer['smesh2_list'].append(smesh2)
            buffer['tsmotion1_list'].append(tsmotion1)
            buffer['tsmotion2_list'].append(tsmotion2)

    # 平滑处理
    if len(buffer['smesh1_list']) >= 7:
        tsmotion_sublist1 = buffer['tsmotion1_list'][-7:]
        tsmotion_sublist2 = buffer['tsmotion2_list'][-7:]
        tsmotion_sublist1[0] = tsmotion_sublist1[0] * 0
        tsmotion_sublist2[0] = tsmotion_sublist2[0] * 0
        with torch.no_grad():
            smooth_out = build_SmoothNet(smooth_net, tsmotion_sublist1, tsmotion_sublist2,
                                        buffer['smesh1_list'][-7:], buffer['smesh2_list'][-7:])
        if buffer['smooth_mesh1'] is None:
            buffer['smooth_mesh1'] = smooth_out['smooth_mesh1']
            buffer['smooth_mesh2'] = smooth_out['smooth_mesh2']
        else:
            buffer['smooth_mesh1'] = torch.cat((buffer['smooth_mesh1'], smooth_out['smooth_mesh1'][:,-1,...].unsqueeze(1)), 1)
            buffer['smooth_mesh2'] = torch.cat((buffer['smooth_mesh2'], smooth_out['smooth_mesh2'][:,-1,...].unsqueeze(1)), 1)

    # 生成拼接帧
    if buffer['smooth_mesh1'] is not None and buffer['idx'] < buffer['smooth_mesh1'].shape[1]:
        stable_list, out_width, out_height = get_stable_sqe(
            buffer['img1_list'], buffer['img2_list'], buffer['smooth_mesh1'], buffer['smooth_mesh2'], 'NORMAL', 'AVERAGE')
        buffer['idx'] += 1
        return stable_list[-1], out_width, out_height
    return None, None, None