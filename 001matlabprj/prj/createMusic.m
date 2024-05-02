function music = createMusic(d_vect,note_vect,fs,start_vect)

%the arguments
%d_vect the vector of note durations
%note_vect the vector of note numbers
%fs the sampling frequency
%start_vect the vector of starting times eg [1,0,0] means the first note
%starts after 1 second, while the second and third notes start at 0sec.
    
    %matlab does not accept to pre allocate A and Time
    %A = zeros(1,length(note_vect));
    %Time = zeros(1,length(note_vect));

    for k = 1:1:length(note_vect)

        [note,time_note] = createNote(d_vect(k),note_vect(k),fs,start_vect(k));

        A{k}=note;
        Time{k}=time_note;

    end
    
    %check the end of each signal
    maxtimes = zeros(1,length(note_vect));
    for i=1:length(note_vect)
        maxtimes(i) = max(Time{1,i});
    end
    
    %append zeros only if necessary to time align the signals
    maximus = max(maxtimes);

    for i=1:length(note_vect)
        A{1,i} = [A{1,i};zeros(ceil(maximus)*fs-ceil(maxtimes(i))*fs,1)];
    end

    %convert cell to matrix
    
    AlmostThere = zeros(ceil(maximus)*fs,length(note_vect));
    for i=1:length(note_vect)
        AlmostThere(:,i) = A{1,i};
    end
    
    %sum columns of the matrix to get the final music
    music = sum(AlmostThere,2);



end