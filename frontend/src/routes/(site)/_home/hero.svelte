<script>
</script>

<section>
	<div class="title">
		You don't need more options. You need the right ones. Every product on Meji is chosen with
		intention — so you spend less time searching and more time enjoying what you buy.
	</div>

	<div class="img">
		<img src="/image/hero_image.png" alt="hero" />
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: center;

		background-color: var(--bg);
		border-radius: 8px;
	}

	.title {
		font-size: 1.8rem;
		font-weight: 800;
		margin: 32px;

		text-align: center;
	}

	.img {
		margin: 32px;
		margin-bottom: 0;
		line-height: 0;
	}

	img {
		height: 300px;
		/* width: 100%; */
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
			align-items: flex-end;
		}

		.title {
			text-align: left;
		}
	}
</style>
