<script>
	import { app } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';

	import Like from './like.svelte';

	let { item } = $props();
	console.log(item);
	

	const prerender = () => {
		app.item = item;
	};
	let src = $state(item.files[0] ? `${item.files[0]}/500` : '/no_photo.png');
</script>

<a href="/{item.slug}" onclick={prerender} onmouseenter={prerender}>
	<div
		class="like"
		onclick={(e) => {
			e.preventDefault();
			e.stopPropagation();
		}}
		role="presentation"
	>
		<Like {item} small></Like>
	</div>
	<img {src} loading="lazy" alt={item.name} onerror={() => (src = '/file_error.png')} />

	<div class="line space nowrap name_rating">
		<div class="name">
			{item.name}
		</div>
		<div class="rating">
			4.5
			<Icon icon="star" size="12" --icon-fill="goldenrod" --icon-stroke="none" />
		</div>
	</div>

	<div class="line cost">
		<div class="price">
			{#if item.price}
				₦{item.price.toLocaleString()}
			{/if}
		</div>
		{#if item.price_old}
			<div class="old_price">
				₦{item.price_old.toLocaleString()}
				<div class="strike"></div>
			</div>
		{/if}
	</div>
</a>

<style>
	a {
		display: block;
		position: relative;
		text-decoration: none;
		color: var(--ft2);
	}

	.like {
		position: absolute;
		top: 0;
		right: 0;
		padding: 8px;
	}

	img {
		width: 100%;
		object-fit: cover;
		aspect-ratio: 1;
		background-color: var(--bg1);
		border-radius: 8px;

		outline: 2px solid transparent;
		outline-offset: 2px;
		transition: outline-color var(--trans);
	}

	a:hover img {
		outline-color: var(--ft1);
	}

	.name_rating {
		align-items: flex-start;
	}

	.name {
		font-size: 0.8rem;
	}

	.cost {
		gap: var(--sp2);
	}
	.price {
		font-weight: 700;
		color: var(--ac1);
		color: var(--ft1);
	}

	.old_price {
		font-size: 0.8rem;
		position: relative;
	}
	.strike {
		position: absolute;
		top: calc(50% - 0.5px);
		left: -3px;
		right: -3px;

		height: 2px;

		transform: rotate(-10deg);
		background-color: red;
		mix-blend-mode: multiply;
	}

	.rating {
		display: flex;
		align-items: center;
		gap: 2px;

		padding: 2px;
		border-radius: 4px;
		background-color: var(--input);

		font-size: 0.8rem;
	}
</style>
