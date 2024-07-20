package com.kushal.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.kushal.model.Candidate;
import com.kushal.model.Vote;
import com.kushal.service.CandidateService;
import com.kushal.service.VoteService;

import java.util.List;

@RestController
@RequestMapping("/api/votes")
public class VoteController {

    @Autowired
    private CandidateService candidateService;

    @Autowired
    private VoteService voteService;

    // Get all candidates for voting
    @GetMapping("/candidates")
    public ResponseEntity<List<Candidate>> getCandidates() {
        List<Candidate> candidates = candidateService.findAll();
        return new ResponseEntity<>(candidates, HttpStatus.OK);
    }

    // Cast a vote
    @PostMapping
    public ResponseEntity<Vote> vote(@RequestParam Long candidateId) {
        Vote vote = new Vote();
        vote.setCandidateId(candidateId);
        // Simulating user ID for simplicity
        vote.setUserId(1L);
        Vote savedVote = voteService.save(vote);
        return new ResponseEntity<>(savedVote, HttpStatus.CREATED);
    }

    // Get voting results
    @GetMapping("/results")
    public ResponseEntity<List<Vote>> getResults() {
        List<Vote> votes = voteService.findAll();
        return new ResponseEntity<>(votes, HttpStatus.OK);
    }
}
