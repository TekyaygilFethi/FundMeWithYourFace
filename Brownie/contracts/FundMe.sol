// SPDX-License-Identifier: MIT

pragma solidity ^0.8.12;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe is Ownable {
    mapping(address => uint256) private addressToAmountFunded;
    address[] funders;
    uint256 public minimumUSDThreshold = 0;
    AggregatorV3Interface priceFeed;

    constructor(address adr) {
        priceFeed = AggregatorV3Interface(adr);
    }

    function fund() public payable {
        uint256 minimumUSD = minimumUSDThreshold * 10**18;
        uint256 conversionRate = getConversionRate(msg.value);

        require(msg.sender != owner(), "You can't fund to yourself!");
        require(conversionRate > minimumUSD, "You need to spend more ETH");

        if (addressToAmountFunded[msg.sender] == 0) {
            funders.push(msg.sender);
        }

        addressToAmountFunded[msg.sender] += msg.value;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = minimumUSDThreshold * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return ((minimumUSD * precision) / price) + 1;
    }

    function setMinimumUSDThreshold(uint256 newAmountInDollars)
        public
        onlyOwner
    {
        minimumUSDThreshold = newAmountInDollars;
    }

    function seeAllFundsAndFunders()
        public
        view
        onlyOwner
        returns (address[] memory, uint256[] memory)
    {
        uint256 len = funders.length;
        uint256[] memory values = new uint256[](len);

        for (uint256 i = 0; i < len; i++) {
            address funderAddress = funders[i];
            values[i] = addressToAmountFunded[funderAddress];
        }
        return (funders, values);
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }

    function getPrice() private view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 amount) private view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * amount) / 1000000000000000000;
        return ethAmountInUsd;
    }
}
