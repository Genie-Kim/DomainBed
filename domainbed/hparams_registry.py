# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import numpy as np

SMALL_IMAGES = ['Debug28', 'RotatedMNIST', 'ColoredMNIST']
IMBALANCE = ['ImbalanceDomainNet']

def _hparams(algorithm, dataset, random_state):
    """
    Global registry of hyperparams. Each entry is a (default, random) tuple.
    New algorithms / networks / etc. should add entries here.
    """

    hparams = {}

    hparams['data_augmentation'] = (True, True)
    hparams['resnet18'] = (True, True)
    hparams['resnet_dropout'] = (0., random_state.choice([0., 0.1, 0.5]))
    hparams['class_balanced'] = (False, False)

    if dataset in IMBALANCE: # for imbalance dataset(no random version support)
        hparams['dataset_version'] = ('MLDG','MLDG')
        hparams['numcls'] = (5,5)
        hparams['testrate'] = (0.2,0.2)
        hparams['valrate'] = (0.1,0.1)
        hparams['targets_fix'] = ([0],[0])
        hparams['imb_data_root'] = (
        '/home/genie/PycharmProjects/DomainBed/domainbed/imbalance_result_output', '/home/genie/PycharmProjects/DomainBed/domainbed/imbalance_result_output')  # 프로젝트 맨 상위 폴더에서 python -m으로 돌릴때..

        hparams['clsordom'] = ('domain','domain')  # make domain imbalance
        hparams['imbrate'] = (10,10)  # The degree of imbalance, expressed as a major/minor value.
        hparams['minor_domain'] = (5,5)



    if dataset not in SMALL_IMAGES:
        hparams['lr'] = (5e-5, 10**random_state.uniform(-5, -3.5))
        if dataset == 'DomainNet':
            hparams['batch_size'] = (32, int(2**random_state.uniform(3, 5)))
        else:
            hparams['batch_size'] = (32, int(2**random_state.uniform(3, 5.5)))
        if algorithm == "ARM":
            hparams['batch_size'] = (8, 8)
    else:
        hparams['lr'] = (1e-3, 10**random_state.uniform(-4.5, -2.5))
        hparams['batch_size'] = (64, int(2**random_state.uniform(3, 9)))

    if dataset in SMALL_IMAGES:
        hparams['weight_decay'] = (0., 0.)
    else:
        hparams['weight_decay'] = (0., 10**random_state.uniform(-6, -2))

    if algorithm in ['DANN', 'CDANN']:
        if dataset not in SMALL_IMAGES:
            hparams['lr_g'] = (5e-5, 10**random_state.uniform(-5, -3.5))
            hparams['lr_d'] = (5e-5, 10**random_state.uniform(-5, -3.5))
        else:
            hparams['lr_g'] = (1e-3, 10**random_state.uniform(-4.5, -2.5))
            hparams['lr_d'] = (1e-3, 10**random_state.uniform(-4.5, -2.5))

        if dataset in SMALL_IMAGES:
            hparams['weight_decay_g'] = (0., 0.)
        else:
            hparams['weight_decay_g'] = (0., 10**random_state.uniform(-6, -2))

        hparams['lambda'] = (1.0, 10**random_state.uniform(-2, 2))
        hparams['weight_decay_d'] = (0., 10**random_state.uniform(-6, -2))
        hparams['d_steps_per_g_step'] = (1, int(2**random_state.uniform(0, 3)))
        hparams['grad_penalty'] = (0., 10**random_state.uniform(-2, 1))
        hparams['beta1'] = (0.5, random_state.choice([0., 0.5]))
        hparams['mlp_width'] = (256, int(2 ** random_state.uniform(6, 10)))
        hparams['mlp_depth'] = (3, int(random_state.choice([3, 4, 5])))
        hparams['mlp_dropout'] = (0., random_state.choice([0., 0.1, 0.5]))
    elif algorithm == "RSC":
        hparams['rsc_f_drop_factor'] = (1/3, random_state.uniform(0, 0.5))
        hparams['rsc_b_drop_factor'] = (1/3, random_state.uniform(0, 0.5))
    elif algorithm == "SagNet":
        hparams['sag_w_adv'] = (0.1, 10**random_state.uniform(-2, 1))
    elif algorithm == "IRM":
        hparams['irm_lambda'] = (1e2, 10**random_state.uniform(-1, 5))
        hparams['irm_penalty_anneal_iters'] = (500, int(10**random_state.uniform(0, 4)))
    elif algorithm == "Mixup":
        hparams['mixup_alpha'] = (0.2, 10**random_state.uniform(-1, -1))
    elif algorithm == "GroupDRO":
        hparams['groupdro_eta'] = (1e-2, 10**random_state.uniform(-3, -1))
    elif algorithm == "MMD" or algorithm == "CORAL":
        hparams['mmd_gamma'] = (1., 10**random_state.uniform(-1, 1))
    elif algorithm == "MLDG":
        hparams['mldg_beta'] = (1., 10**random_state.uniform(-1, 1))
    elif algorithm == "MTL":
        hparams['mtl_ema'] = (.99, random_state.choice([0.5, 0.9, 0.99, 1.]))
    elif algorithm == "VREx":
        hparams['vrex_lambda'] = (1e1, 10**random_state.uniform(-1, 5))
        hparams['vrex_penalty_anneal_iters'] = (500, int(10**random_state.uniform(0, 4)))
    elif algorithm == "MFM_MLDG":
        hparams['small_meta_data'] = (True, True)
        hparams["mod_lr"] = (1e-4,1e-4)
        hparams['num_smallmetaset'] = (7,7)
        hparams['hidden_neurons'] = (256,256)
        hparams['mldg_beta'] = (1., 10 ** random_state.uniform(-1, 1))
        hparams['mod_in_outer'] = (True,True) # modulation in outer update
        hparams['mixdom_metaset'] = (False,True)
        if hparams['mixdom_metaset'][0]: # if mixing
            hparams['small_batch'] = (7,7) # final batch number = x*도메인개수
        else:
            hparams['small_batch'] = (30,30)

    elif algorithm == "MWN_MLDG":
        hparams['small_meta_data'] = (True, True)
        hparams["mod_lr"] = (1e-3,1e-3)
        hparams['num_smallmetaset'] = (7,7)
        hparams['hidden_neurons'] = (100,100)
        hparams['mldg_beta'] = (1., 10 ** random_state.uniform(-1, 1))
        hparams['mod_in_outer'] = (False,True) # modulation in outer update
        hparams['mixdom_metaset'] = (True,True)
        if hparams['mixdom_metaset'][0]: # if mixing
            hparams['small_batch'] = (7,7) # final batch number = x*도메인개수
        else:
            hparams['small_batch'] = (30,30)
    # 특정한 순서를 두고 hyper parameter search를 하고 싶을 때는
    # hlist = [0.1,0.01,0.0001]
    # hiter = iter(hlist)
    # 그리고 random hyper parameter 자리에 next(hiter)를 하면 된다.

    return hparams

def default_hparams(algorithm, dataset):
    dummy_random_state = np.random.RandomState(0)
    return {a: b for a,(b,c) in
        _hparams(algorithm, dataset, dummy_random_state).items()}

def random_hparams(algorithm, dataset, seed):
    random_state = np.random.RandomState(seed)
    return {a: c for a,(b,c) in _hparams(algorithm, dataset, random_state).items()}
