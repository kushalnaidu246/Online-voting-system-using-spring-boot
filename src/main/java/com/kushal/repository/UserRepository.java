package com.kushal.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.kushal.model.User;

public interface UserRepository extends JpaRepository<User, Long> {

}
