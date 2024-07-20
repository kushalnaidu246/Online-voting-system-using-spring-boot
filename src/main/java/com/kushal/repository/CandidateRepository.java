package com.kushal.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.kushal.model.Candidate;

public interface CandidateRepository extends JpaRepository<Candidate, Long> {
}

