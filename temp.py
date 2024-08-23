
    for p in processes:
        p.start()

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating processes")
        running.value = False
        for p in processes:
            p.terminate()
            p.join()

