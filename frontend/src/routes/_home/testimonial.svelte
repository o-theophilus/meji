<script>
	import { RoundButton } from '$lib/button';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';
	import Rating from '../[slug]/review/rating.svelte';

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
			comment: 'I didn\'t have to second guess anything. Everything felt intentional.',
			rating: 4.5
		},
		{
			name: 'Tunde O.',
			photo: 'user3.png',
			comment: 'Fast delivery and exactly what I expected. That\'s rare these days.',
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
			comment: 'Finally a store that doesn\'t overwhelm you with options.',
			rating: 5
		},
		{
			name: 'Kemi A.',
			photo: 'user8.png',
			comment: 'Everything feels refined. You can trust what you\'re buying.',
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
			comment: 'Great experience overall. I\'ll definitely be coming back.',
			rating: 4.5
		}
	];

	let index = $state(0);
	let prev_index = $derived((index - 1 + testimonials.length) % testimonials.length);
	let next_index = $derived((index + 1) % testimonials.length);
	const next = () => (index = (index + 1) % testimonials.length);
	const prev = () => (index = (index - 1 + testimonials.length) % testimonials.length);
</script>

<div class="margin">
	<div class="title">Trusted by customers who value simplicity</div>
	<br />
	<br />

	<div class="carousel">
		<RoundButton icon="chevron-left" onclick={prev}></RoundButton>
		<div class="cards">
			{#each [prev_index, index, next_index] as idx, pos (idx)}
				<div
					class="card"
					class:active={pos === 1}
					animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}
					transition:slide
				>
					<div class="bold">{testimonials[idx].name}</div>
					<div class="details">
						<Rating value={testimonials[idx].rating}></Rating>
						<div>{testimonials[idx].comment}</div>
					</div>
				</div>
			{/each}
		</div>

		<div class="card_one">
			<div class="card">
				<div class="bold">{testimonials[index].name}</div>
				<div class="details">
					<Rating value={testimonials[index].rating}></Rating>
					<div>{testimonials[index].comment}</div>
				</div>
			</div>
		</div>
		<RoundButton icon="chevron-right" onclick={next}></RoundButton>
	</div>
</div>

<style>
	.margin {
		margin: 160px 0;
	}

	.title {
		font-size: 2rem;
		text-align: center;
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
		justify-content: center;
		gap: 20px;
	}

	.cards {
		display: flex;
		align-items: center;
		gap: 20px;

		&:not(.active) {
			display: none;
			@media screen and (min-width: 720px) {
				display: flex;
			}
		}
	}

	.card_one {
		display: flex;
		align-items: center;
		gap: 20px;

		&:not(.active) {
			display: block;
			@media screen and (min-width: 720px) {
				display: none;
			}
		}
	}

	.card {
		background-color: var(--bg3);
		padding: 24px 16px;
		border-radius: 8px;
		text-align: center;
		width: 100%;

		.details {
			display: grid;
			grid-template-rows: 0fr;

			div {
				overflow: hidden;
			}

			margin-top: 12px;
			display: flex;
			align-items: center;
			flex-direction: column;
			gap: 4px;
		}
	}
</style>
