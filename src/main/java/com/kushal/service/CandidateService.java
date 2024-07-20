package com.kushal.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.kushal.model.Candidate;
import com.kushal.repository.CandidateRepository;

@Service
public class CandidateService {

    @Autowired
    private CandidateRepository candidateRepository;

    public List<Candidate> findAll() {
        return candidateRepository.findAll();
    }

    public Candidate save(Candidate candidate) {
        return candidateRepository.save(candidate);
    }
}
