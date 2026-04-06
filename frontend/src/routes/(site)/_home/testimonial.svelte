<script>
	import { flip } from 'svelte/animate';

	let testimonials = [
		{
			name: 'Daniel A.',
			photo: 'user1.png',
			comment: 'Clean experience from start to finish. No distractions, just quality products.',
			rating: 5
		},
		{
			name: 'Chioma K.',
			photo: 'user2.png',
			comment: 'I didn’t have to second guess anything. Everything felt intentional.',
			rating: 4.5
		},
		{
			name: 'Tunde O.',
			photo: 'user3.png',
			comment: 'Fast delivery and exactly what I expected. That’s rare these days.',
			rating: 5
		},
		{
			name: 'Amara E.',
			photo: 'user4.png',
			comment: 'I like how simple everything is. It makes shopping feel effortless.',
			rating: 4.5
		},
		{
			name: 'Ibrahim S.',
			photo: 'user5.png',
			comment: 'You can tell the products are carefully selected. Nothing feels random.',
			rating: 5
		},
		{
			name: 'Zainab M.',
			photo: 'user6.png',
			comment: 'Smooth checkout, reliable service, and great product quality.',
			rating: 4.5
		},
		{
			name: 'Victor U.',
			photo: 'user7.png',
			comment: 'Finally a store that doesn’t overwhelm you with options.',
			rating: 5
		},
		{
			name: 'Kemi A.',
			photo: 'user8.png',
			comment: 'Everything feels refined. You can trust what you’re buying.',
			rating: 4.5
		},
		{
			name: 'Sadiq R.',
			photo: 'user9.png',
			comment: 'Simple, fast, and reliable. Exactly how online shopping should be.',
			rating: 5
		},
		{
			name: 'Ngozi N.',
			photo: 'user10.png',
			comment: 'Great experience overall. I’ll definitely be coming back.',
			rating: 4.5
		}
	];

	let current_index = $state(0);

	let prev_index = $derived((current_index - 1 + testimonials.length) % testimonials.length);
	let next_index = $derived((current_index + 1) % testimonials.length);

	function next() {
		current_index = (current_index + 1) % testimonials.length;
	}

	function prev() {
		current_index = (current_index - 1 + testimonials.length) % testimonials.length;
	}
</script>

<div class="margin">
	<div class="title">Testimonials</div>
	<br />

	<div class="carousel">
		<button class="nav-btn" onclick={prev}>&lt;</button>
		<div class="cards">
			{#each [prev_index, current_index, next_index] as idx, pos}
				<div class="card" class:active={pos === 1} transition:flip={{ duration: 300 }}>
					<div class="bold">{testimonials[idx].name}</div>
					{#if pos === 1}
						<div>{testimonials[idx].comment}</div>
						<div>Rating: {testimonials[idx].rating} / 5</div>
					{/if}
				</div>
			{/each}
		</div>
		<button class="nav-btn" onclick={next}>&gt;</button>
	</div>
</div>

<style>
	.margin {
		margin: 160px 0;
	}

	.title {
		font-size: 2rem;
		color: var(--ft1);
		line-height: 120%;
		font-weight: 600;
	}

	.bold {
		font-weight: 600;
		font-size: 1.2rem;
		color: var(--ft1);
	}

	.carousel {
		display: flex;
		align-items: center;
		gap: 20px;
		justify-content: center;
	}

	.nav-btn {
		background: none;
		border: none;
		font-size: 2rem;
		cursor: pointer;
		color: var(--ft1);
		padding: 10px;
	}

	.cards {
		display: flex;
		gap: 20px;
		align-items: center;
	}

	.card {
		background-color: var(--bg3);
		padding: 24px 16px;
		border-radius: 8px;
		min-width: 200px;
		text-align: center;
		transition: transform 0.3s ease;
	}

	.card.active {
		transform: scale(1.1);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	}
</style>
