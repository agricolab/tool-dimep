Decomposition Simulation
------------------------

The following is a annotated part of the source code we used for the simulation of the decomposition to answer the questions how many trials would be required to achieve a reliable decomposition.

.. code-block:: python



    def get_score(data):        
        if data.shape[1] > 1:
            # if we use at least two trials for PCA, we flip the trials to 
            # make sure the first component aligns in direction    
            flipper = orient_principal(data)
            data = flipper * data
            # and calculate the score (s)
            c, s, v = pca_largest(data)        
        else: # if we have only one trial, this is the first component
            s = data
        # the sign of a score/coefficient pair is arbitrary  
        # if the positive peak in the score occurs later than the negative 
        # peak, we invert the score to align all scores across all bootstrap
        # repetitions
        if np.argmax(s[:, 0]) > np.argmin(s[:, 0]):
            return -s[:, 0]
        else:
            return s[:, 0]


    # assuming that data is the [samples x trials] matrix of all trials across 
    # all subjects, we remembert the maximal number of trials NT and define 
    # the range of trials picked over which we want to explore the simulation

    NT = data.shape[1]
    ratio = np.hstack(
        (
            np.arange(2, 10, 1, dtype=int),
            np.arange(10, 100, 10, dtype=int),
            np.arange(100, 1000, 100, dtype=int),
        )
    )

    As = []    
    for pratio in ratio:
        # We balanced the number of repetitions, i.e. we run more repetitions
        # for small sample sizes to increase the accuracy and less repetitions 
        # for high sample sizes to reduce computational cost.
        # Additionally, the maximal number of sample sizes is bound to the 
        # maximally available trials in the dataset.
        reps = int(NT / pratio)
        with tqdm(
            total=reps, desc=f"Bootstrap PCA reliability {pratio}"
        ) as pbar:
            A = []
            for rep in range(reps):                                            
                shuffled = np.random.choice(range(NT), NT)

                # train the first score on the partial dataset
                pick = shuffled[0:pratio]
                s1 = get_score(np.take(data, pick, axis=1))

                # train the second score on another part of the dataset
                pick = shuffled[pratio : 2 * pratio]
                s2 = get_score(np.take(data, pick, axis=1).copy())

                # calculate their correlation coefficient
                a, _ = pearsonr(s1, s2)
                A.append(a)
                pbar.update(1)

        # average the correlation coefficient under transformation 
        # to account for the bounds and non-normality         
        As.append(np.tanh(np.arctanh(A).mean()))

    fig, ax = plt.subplots(1, 1, figsize=(6, 4), dpi=300)
    ax.semilogx(ratio, As, "k")
    ax.set_ylabel("Waveform Reproducibility")
    ax.set_xlabel("Available Trials")
    ax.grid()