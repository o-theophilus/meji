<script>
	import { app } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';

	import Like from './like.svelte';
	import Rating from '../[slug]/review/rating.svelte';

	let { item } = $props();

	const date_created = new Date(item.date_created);
	const today = new Date();
	const oneWeekAgo = new Date();
	oneWeekAgo.setDate(today.getDate() - 7);

	const prerender = () => {
		app.item = item;
	};
</script>

<a href="/{item.slug}" onclick={prerender} onmouseenter={prerender}>
	<div class="img">
		{#if item.status == 'active'}
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
			{#if item.quantity == 0}
				<div class="unavailable">Out of stock</div>
			{/if}
		{:else}
			<div class="unavailable">Unavailable</div>
		{/if}

		{#if item.rating > 0}
			<div class="rating">
				<Rating value={item.rating} mini></Rating>
			</div>
		{/if}
		{#if date_created >= oneWeekAgo}
			<div class="new">New</div>
		{/if}
		<img
			src="{item.files[0]}/500"
			loading="lazy"
			alt={item.name}
			onerror={(e) => (e.target.src = '/no_photo.png')}
		/>
	</div>

	<div class="details">
		<div class="name">
			{item.name}
		</div>

		<div class="cost">
			<div class="price">
				{#if Number(item.price)}
					₦{Number(item.price).toLocaleString()}
				{/if}
			</div>

			{#if item.discount > 15}
				{#if Number(item.price) && Number(item.price_old)}
					<div class="discount">
						{Number(item.discount).toFixed(0)}% off
					</div>
				{/if}
			{:else if Number(item.price_old)}
				<div class="old_price">
					₦{Number(item.price_old).toLocaleString()}
					<div class="strike"></div>
				</div>
			{/if}
		</div>
	</div>
</a>

<style>
	a {
		display: block;
		text-decoration: none;
		color: var(--ft2);
		background-color: var(--bg3);
		border-radius: 8px;
		overflow: hidden;
		outline: 1px solid var(--ol);
		height: 100%;

		--red: rgb(186, 63, 63);

		transition: outline-color 0.2s ease-in-out;

		&:hover {
			outline-color: var(--ft1);
		}
	}

	.img {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;

		& .like {
			position: absolute;
			top: 0;
			right: 0;
			padding: 8px;
		}

		& .unavailable {
			position: absolute;
			padding: 8px;
			outline: 1px solid red;
			background-color: color-mix(in srgb, red, transparent 40%);
			border-radius: 8px;
			color: var(--ft1);
			transform: rotate(-25deg);
		}

		& .rating {
			position: absolute;
			bottom: 8px;
			right: 8px;
			--ratig-padding: 2px 4px;
			--rating-background-color: rgba(0, 0, 0, 0.6);
		}

		& .new {
			position: absolute;
			left: -36px;
			top: 4px;

			transform: rotate(-45deg);

			background-color: var(--red);
			color: white;
			font-size: 0.9rem;
			width: 100px;
			text-align: center;
		}

		& img {
			width: 100%;
			object-fit: cover;
			aspect-ratio: 1;
			outline-offset: 2px;
			transition: outline-color 0.2s ease-in-out;
			display: block;
		}
	}

	.details {
		padding: 8px 12px;

		& .name {
			font-size: 0.9rem;
			line-height: 120%;
		}

		& .cost {
			display: flex;
			align-items: center;
			flex-wrap: wrap;
			gap: 0 12px;
			margin-top: 4px;

			& .price {
				font-size: 1.1rem;
				font-weight: 700;
				color: var(--ac1);
				color: var(--ft1);
			}

			& .old_price {
				font-size: 0.9rem;
				position: relative;
				& .strike {
					position: absolute;
					top: calc(50% - 0.5px);
					left: -3px;
					right: -3px;

					height: 2px;

					transform: rotate(-10deg);
					background-color: var(--red);
				}
			}

			& .discount {
				line-height: 100%;
				font-size: 0.9rem;

				padding: 2px 4px;
				border-radius: 4px;
				color: var(--red);
				background-color: var(--bg1);
			}
		}
	}
</style>
