<div class="bubble">
	<div class="text">
		<span> Offer </span>
		20% OFF
	</div>
</div>

<style>
	.bubble {
		--height: 50px;

		display: flex;
		justify-content: center;
		align-items: center;

		background-color: red;
		width: 100px;
		height: var(--height);

		color: white;

		border-radius: calc(var(--height) / 2);
		font-size: larger;
	}

	.bubble * {
		display: flex;
		flex-direction: column;
		justify-content: center;
		line-height: 100%;
	}

	.bubble::after {
		position: absolute;
		top: calc(100% - 2px);
		left: 20px;

		content: '';
		border: 10px solid red;

		border-bottom-color: transparent;
		border-right-color: transparent;
	}

	.bubble span {
		font-size: 0.7rem;
	}
</style>
