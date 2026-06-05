// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract SoulboundProvenance is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    struct Provenance {
        bytes32 contentHash;
        string community;
        string language;
        uint256 recordedAt;
        bool aiTrainingAllowed;
    }

    mapping(uint256 => Provenance) public provenance;
    address public relayer;

    event ProvenanceMinted(
        uint256 indexed tokenId,
        bytes32 contentHash,
        string community,
        string language,
        uint256 recordedAt,
        bool aiTrainingAllowed
    );

    constructor(address _relayer) ERC721("FirstVoice Provenance", "FVP") {
        relayer = _relayer;
    }

    modifier onlyRelayer() {
        require(msg.sender == relayer, "Only relayer can mint");
        _;
    }

    function mint(
        address to,
        bytes32 contentHash,
        string memory community,
        string memory language,
        uint256 recordedAt,
        bool aiTrainingAllowed
    ) external onlyRelayer returns (uint256 tokenId) {
        tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        provenance[tokenId] = Provenance(
            contentHash,
            community,
            language,
            recordedAt,
            aiTrainingAllowed
        );
        emit ProvenanceMinted(
            tokenId,
            contentHash,
            community,
            language,
            recordedAt,
            aiTrainingAllowed
        );
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override {
        require(from == address(0), "Soulbound: non-transferable");
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }
}
