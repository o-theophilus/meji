<section>
	<div class="title_block">
		<div class="title"><slot name="title" /></div>
		<slot name="desc" />
	</div>
	<div class="form">
		<slot />
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
		max-width: 500px;
	}

	@media screen and (min-width: 800px) {
		section {
			max-width: 800px;
			flex-direction: unset;
		}
		.title_block {
			width: 300px;
		}
		.form {
			width: 100%;
		}
	}

	.title_block {
		display: flex;
		gap: var(--sp1);
		flex-direction: column;

		padding: var(--sp3);
		background-color: var(--cl1);

		color: var(--light_color);
	}

	.title {
		font-size: 1.2rem;
		font-weight: bold;
	}

	.form {
		padding: var(--sp3);
		background-color: var(--ac4);
	}
</style>
