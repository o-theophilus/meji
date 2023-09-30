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
			go('tag');
		}}
	>
		Tags
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
	<!-- <button
		on:click={() => {
			go();
		}}
	>
		Q&A
	</button> -->
	<button
		on:click={() => {
			go("contact");
		}}
	>
		Contact
	</button>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp2);
		padding: var(--sp3);
		padding-top: calc(var(--sp3) * 2);

		justify-content: center;
		font-weight: 500;

		flex-wrap: wrap;
	}

	button {
		all: unset;
		cursor: pointer;
	}

	button:hover {
		color: var(--cl1);
	}
</style>
