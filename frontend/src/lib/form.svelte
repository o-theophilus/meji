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
		display: flex;
		flex-direction: column;
	}

	.title {
		padding: var(--sp3);

		background-color: var(--cl1);
		color: var(--ac6_);

		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}

	form {
		background-color: var(--ac6);
		padding: var(--sp3);
		color: var(--ac2);
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
		}
		.title {
			width: 300px;
		}
		form {
			width: 100%;
		}
	}
</style>
