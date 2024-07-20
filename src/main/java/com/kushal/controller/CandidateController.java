package com.kushal.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.kushal.model.Candidate;
import com.kushal.service.CandidateService;

import java.util.List;

@RestController
@RequestMapping("/api/candidates")
public class CandidateController {

    @Autowired
    private CandidateService candidateService;

    // Get all candidates
    @GetMapping
    public ResponseEntity<List<Candidate>> getCandidates() {
        List<Candidate> candidates = candidateService.findAll();
        return new ResponseEntity<>(candidates, HttpStatus.OK);
    }

    // Add a new candidate
    @PostMapping
    public ResponseEntity<Candidate> addCandidate(@RequestBody Candidate candidate) {
        Candidate savedCandidate = candidateService.save(candidate);
        return new ResponseEntity<>(savedCandidate, HttpStatus.CREATED);
    }
}
