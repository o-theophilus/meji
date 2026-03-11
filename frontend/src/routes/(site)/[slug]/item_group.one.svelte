<script>
	import { app } from '$lib/store.svelte.js';

	let { item, refresh, can_hide } = $props();

	const prerender = (x) => {
		app.item = x;
	};
</script>

<a
	class="name"
	class:can_hide
	href="/{item.slug}"
	onclick={() => {
		prerender(item);
		refresh(item);
	}}
	onmouseenter={() => prerender(item)}
>
	<img
		src="{item.files[0]}/64"
		loading="lazy"
		alt={item.name}
		onerror={(e) => (e.target.src = '/no_photo.png')}
	/>
	<div class="details">
		<div class="name">
			{item.name}
		</div>

		<div class="price">
			{#if Number(item.price)}
				₦{Number(item.price).toLocaleString()}
			{/if}
		</div>
	</div>
</a>

<style>
	a {
		display: flex;
		gap: 8px;

		background-color: var(--bg3);
		padding: 8px;
		border-radius: 8px;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
		text-decoration: none;
		color: var(--ft2);

		transition: background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
		}

		&.can_hide {
			display: none;
		}

		@media screen and (min-width: 600px) {
			&.can_hide {
				display: flex;
			}
		}

		& img {
			width: 48px;
			aspect-ratio: 1;
			object-fit: cover;
			display: block;
			border-radius: 4px;
		}

		& .details {
			display: flex;
			flex-direction: column;
			justify-content: flex-end;

			& .name {
				text-decoration: none;
				color: var(--ft1);
				font-size: 0.8rem;
				line-height: 120%;

				transition: color 0.2s ease-in-out;
			}

			& .price {
				font-size: 0.9rem;
				font-weight: 700;
				color: var(--ft1);
			}
		}
	}
</style>
