<section>
	<div class="title">
		<slot name="title" />
	</div>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<slot />
	</form>
</section>

<style>
	section {
		margin: auto;

		display: flex;
		flex-direction: column;
		/* min-width: 100%; */
		/* width: 500px; */
		/* width: min(100%, 500px); */
	}
	form {
		background-color: var(--ac5);
	}

	@media screen and (min-width: 800px) {
		section {
			/* max-width: 800px; */
			flex-direction: unset;
		}
		.title {
			width: 300px;
		}
		form {
			width: 100%;
		}
	}

	.title {
		padding: var(--sp3);

		background-color: var(--cl1);
		color: var(--ac5_);

		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}

	form {
		padding: var(--sp3);
	}
</style>
