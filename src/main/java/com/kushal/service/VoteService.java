package com.kushal.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.kushal.model.Vote;
import com.kushal.repository.VoteRepository;

@Service
public class VoteService {

    @Autowired
    private VoteRepository voteRepository;

    public Vote save(Vote vote) {
        return voteRepository.save(vote);
    }

    public List<Vote> findAll() {
        return voteRepository.findAll();
    }
}

