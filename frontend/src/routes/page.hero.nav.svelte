<script>
	const go = (name) => {
		document.querySelector(`#${name}`).scrollIntoView({
			behavior: 'smooth'
		});
	};
</script>

<section>
	<button
		on:click={() => {
			go('top');
		}}
	>
		Home
	</button>
	<button
		on:click={() => {
			go('category');
		}}
	>
		Categories
	</button>
	<button
		on:click={() => {
			go('new_arrivals');
		}}
	>
		New Arrivals
	</button>
	<button
		on:click={() => {
			go('offers');
		}}
	>
		Offers
	</button>
	<button
		on:click={() => {
			go('about');
		}}
	>
		About Us
	</button>
	<button
		on:click={() => {
			go();
		}}
	>
		Q&A
	</button>
	<button
		on:click={() => {
			go();
		}}
	>
		Contact
	</button>
</section>

<style>
	section {
		display: flex;
		gap: var(--gap2);
		padding: var(--gap3);
		padding-top: calc(var(--gap3) * 2);

		justify-content: center;
		font-weight: 500;

		flex-wrap: wrap;
	}

	button {
		all: unset;
		cursor: pointer;
	}

	button:hover {
		color: var(--color1);
	}
</style>