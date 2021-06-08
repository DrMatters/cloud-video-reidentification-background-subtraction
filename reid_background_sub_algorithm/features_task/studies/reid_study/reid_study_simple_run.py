import torchreid


def main():
    # torchreid.data.register_video_dataset('saivt_softbio',
    #                                       saivt_softbio.Saivt_SoftBio)

    datamanager = torchreid.data.VideoDataManager(
        root='E:\\datasets',
        sources='ilidsvid',
        targets='ilidsvid',
        height=256,
        width=128,
        batch_size_train=2,
        batch_size_test=2,
        transforms=['random_flip', 'random_crop'],
        train_sampler='RandomSampler'
    )

    model = torchreid.models.build_model(
        name='osnet_x0_25',
        num_classes=datamanager.num_train_pids,
        loss='triplet',
        pretrained=True
    )

    optimizer = torchreid.optim.build_optimizer(
        model,
        optim='adam',
        lr=0.0003
    )

    scheduler = torchreid.optim.build_lr_scheduler(
        optimizer,
        lr_scheduler='single_step',
        stepsize=20
    )

    engine = torchreid.engine.VideoTripletEngine(
        datamanager,
        model,
        optimizer=optimizer,
        scheduler=scheduler,
        label_smooth=True
    )

    engine.run(
        save_dir='log/osnet',
        max_epoch=60,
        eval_freq=10,
        print_freq=1,
        test_only=False
    )


if __name__ == "__main__":
    main()
