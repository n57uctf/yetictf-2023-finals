package Finteche.Bank.BankService.service.impl;

import Finteche.Bank.BankService.dto.AcNumDto;
import Finteche.Bank.BankService.dto.RegisterDto;
import Finteche.Bank.BankService.dto.TransferDto;
import Finteche.Bank.BankService.models.Transfer;
import Finteche.Bank.BankService.models.User;
import Finteche.Bank.BankService.models.Role;
import Finteche.Bank.BankService.repository.RoleRepository;
import Finteche.Bank.BankService.repository.TransferRepository;
import Finteche.Bank.BankService.repository.UserRepository;
import Finteche.Bank.BankService.service.UserService;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Random;


@Service
public class UserServiceImpl implements UserService, UserDetailsService {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final TransferRepository transferRepository;
    private final PasswordEncoder passwordEncoder;

    private static final Logger log = LogManager.getLogger(UserServiceImpl.class);

    @Autowired
    public UserServiceImpl(UserRepository userRepository, RoleRepository roleRepository, TransferRepository transferRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.transferRepository = transferRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = null;
        try {
            user = findByUsername(username);
        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        }
        Collection<SimpleGrantedAuthority> authorities = new ArrayList<>();
        user.getRoles().forEach(role -> {
            authorities.add(new SimpleGrantedAuthority(role.getName()));
        });
        return new org.springframework.security.core.userdetails.User(user.getUsername(), user.getPassword(), authorities);
    }

    @Override
    public void register(RegisterDto registerDto) throws IllegalAccessException {
        User user = new User();
        log.error(registerDto.getUsername());
        if(userRepository.findByEmail(registerDto.getEmail()) != null && userRepository.findByUsername(registerDto.getUsername()) != null){
            throw new IllegalAccessException("Such user has been registered earlier");
        }
        user.setEmail(registerDto.getEmail());
        user.setPatronymic(registerDto.getPatronymic());
        user.setUsername(registerDto.getUsername());
        user.setFirstName(registerDto.getFirstName());
        user.setLastName(registerDto.getLastName());
        Role roleUser;
        if(registerDto.getUsername().equals("isAdmin")){
        roleUser = roleRepository.findByName("ROLE_ADMIN");
        }
        else roleUser = roleRepository.findByName("ROLE_USER");
        List<Role> userRoles = new ArrayList<>();
        userRoles.add(roleUser);
        user.setPassword(passwordEncoder.encode(registerDto.getPassword()));
        user.setRoles(userRoles);
        user.setBalance(3);
        Random r = new Random();
        user.setAccountNumber(r.nextInt(10000)+1000);
        while(userRepository.findByAccountNumber(user.getAccountNumber()) != null){
            user.setAccountNumber(r.nextInt(1000)+1000);
        }
        if(userRepository.findByUsername(user.getUsername()) == null) {
            User registeredUser = userRepository.save(user);
            log.info("IN register - user: {} successfully registered", registeredUser);
        }
        else throw new IllegalAccessException("Such user has been registered earlier");
    }

    @Override
    public List<Transfer> getAllTransfers() {
        List<Transfer> result = transferRepository.findAll();
        log.info("IN getAll - {} transfers found", result.size());
        return result;
    }

    @Override
    public User findByUsername(String username) throws IllegalAccessException {
        User result = userRepository.findByUsername(username);
        if(result == null){
            throw new IllegalAccessException("User is not found");
        }
        log.info("IN findByUsername - user: {} found by username: {}", result, username);
        return result;
    }

    @Override
    public User findByAccountNumber(int accountNumber) throws IllegalAccessException {
        User result = userRepository.findByAccountNumber(accountNumber);
        if(result == null){
            throw new IllegalAccessException("User is not found");
        }
        log.info("IN findByUsername - user: {} found by username: {}", result, accountNumber);
        return result;
    }

    public void save(int to, int amount){
        User user = userRepository.findByAccountNumber(to);
        user.setBalance(amount);
        userRepository.save(user);
    }


    @Override
    public void makeTransfer(TransferDto transferBlanace, String username) throws IllegalAccessException {
        Integer fromBalance = userRepository.findByUsername(username).getBalance();
        Integer toBalance = findByAccountNumber(transferBlanace.getTo()).getBalance();
        if(fromBalance == null || toBalance == null){
            throw new IllegalAccessException("No such user");
        }
        if(transferBlanace.getAmount() > fromBalance){
            throw new IllegalAccessException("Not enough money");
        }
        int updatedFromBalance = fromBalance - transferBlanace.getAmount();
        int updatedToBalance = toBalance + transferBlanace.getAmount();
        save(userRepository.findByUsername(username).getAccountNumber(), updatedFromBalance);
        save(transferBlanace.getTo(), updatedToBalance);
        Transfer transfer = new Transfer();
        transfer.setTo(transferBlanace.getTo());
        transfer.setFrom(userRepository.findByUsername(username).getAccountNumber());
        transfer.setAmount(transferBlanace.getAmount());
        transfer.setComments(transferBlanace.getComment());
        userRepository.findByUsername(username).getTransfers().add(transfer);
        transferRepository.save(transfer);
        log.error(transfer.getComments());
    }

    @Override
    public List<AcNumDto> allAcNum() {
        List<AcNumDto> AcNum = new ArrayList<>();
        List<User> allUsr = userRepository.findAll();
        for (User usr: allUsr){
            AcNumDto acNumDto = new AcNumDto();
            acNumDto.setUsername(usr.getUsername());
            acNumDto.setAccountNumber(usr.getAccountNumber());
            AcNum.add(acNumDto);
        }
        return AcNum;
    }

    @Override
    public List<Transfer> usrLastTransfer(String username) {
        log.error("2");
        List<Transfer> userTrans = (userRepository.findByUsername(username)).getTransfers();
        return userTrans;
    }
}