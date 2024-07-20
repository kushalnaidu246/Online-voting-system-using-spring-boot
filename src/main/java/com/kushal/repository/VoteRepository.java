package com.kushal.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.kushal.model.Vote;

public interface VoteRepository extends JpaRepository<Vote, Long> {

}
