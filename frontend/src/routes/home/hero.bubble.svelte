<div class="bubble">
	<div>
		<span> Offer </span>
		<br />
		20% OFF
	</div>
</div>

<style>
	.bubble {
		--height: 50px;

		display: flex;
		justify-content: center;
		align-items: center;

		background-color: var(--secondary);
		width: 100px;
		height: var(--height);

		color: var(--ac5_);

		border-radius: calc(var(--height) / 2);
		font-size: 1.2rem;
		line-height: 14px;
	}

	.bubble::after {
		position: absolute;
		top: calc(100% - 2px);
		left: 20px;

		content: '';
		border: 10px solid var(--secondary);

		border-bottom-color: transparent;
		border-right-color: transparent;
	}

	.bubble span {
		font-size: x-small;
	}
</style>
