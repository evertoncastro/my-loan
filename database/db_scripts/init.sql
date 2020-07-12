create database if not exists loan;

USE loan;

CREATE TABLE `loan_request` (
  `id` varchar(100) NOT NULL,
  `cpf` varchar(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `birthdate` date NOT NULL,
  `amount` float DEFAULT NULL,
  `terms` int(11) DEFAULT NULL,
  `income` float DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `result` varchar(15) DEFAULT NULL,
  `refused_policy` varchar(15) DEFAULT NULL,
  `approved_amount` float DEFAULT NULL,
  `approved_terms` int(11) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
