<script>
	import { page } from '$app/state';
	import { LinkArrow } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { page_state } from '$lib/store.svelte.js';
	import One from '../shop/item.svelte';

	let _group = [
		{
			title: 'Best Sellers',
			items: [], // TODO: Best Sellers
			order: 'rating',
			icon: 'trending-up'
		},
		{
			title: 'New Arrivals',
			items: page.data.new_arrivals,
			order: 'latest',
			icon: 'sparkles'
		},
		{
			title: 'Discount Items',
			items: page.data.discount,
			order: 'discount',
			icon: 'badge-percent'
		}
	];

	let group = [];
	for (const x of _group) {
		if (x.items.length) group.push(x);
	}
	let active = $state(0);
</script>

{#if group.length}
	<section>
		<div class="title">Featured Collection{group.length > 1 ? 's' : ''}</div>

		{#if group.length > 1}
			<div class="tabs">
				{#each group as g, i}
					{#if g.items.length}
						<button onclick={() => (active = i)} class:active={active == i}>
							<Icon icon={g.icon}></Icon>
							{g.title}
						</button>
					{/if}
				{/each}
			</div>
		{/if}

		{#if group[active].items.length}
			<div class="view_more">
				<LinkArrow
					onclick={() => page_state.goto('shop', { order: group[active].order })}
					--link-font-size="0.8rem"
				>
					See All
				</LinkArrow>
			</div>

			<div class="grid">
				{#each group[active].items as item, i (item.key)}
					<div class="item" class:can_hide={i > 5}>
						<One {item}></One>
					</div>
				{/each}
			</div>
		{/if}
	</section>
{/if}

<style>
	section {
		margin: 160px 0;
		padding: 16px;
		background-color: var(--bg);
		border-radius: 8px;
		overflow: hidden;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
		position: relative;
		z-index: 0;
		&::before {
			content: '';
			position: absolute;
			inset: 0;

			background-image: url('/image/bg.png');
			background-position: center;

			opacity: 0.2;
			z-index: -1;
		}
	}

	.title {
		margin-bottom: 16px;
		background-color: transparent;
		border-radius: 8px;
		font-size: 2rem;
		color: var(--ft1);
		font-weight: 600;
		padding: 8px;
	}

	.tabs {
		display: flex;
		border-bottom: 1px solid var(--ol);

		position: relative;
		z-index: 0;

		&::before {
			content: '';
			position-anchor: --active;

			position: absolute;
			bottom: calc(anchor(bottom) - 2px);
			right: anchor(right);
			left: anchor(left);
			height: 4px;
			z-index: 1;

			background-color: var(--cl1);
			border-radius: var(--toggle-border-radius, 4px);

			transition:
				right 0.2s ease-in-out,
				left 0.2s ease-in-out;
		}

		button {
			all: unset;
			cursor: pointer;

			display: flex;
			gap: 8px;
			align-items: center;

			background-color: transparent;
			border-radius: 8px;
			/* font-size: 2rem; */
			font-weight: 600;
			padding: 8px;

			transition: background-color 0.2s ease-in-out;

			&.active {
				anchor-name: --active;
				color: var(--ft1);
				fill: var(--ft1);
			}

			&:hover {
				color: var(--ft1);
				fill: var(--ft1);
				background-color: var(--bg2);
			}
		}
	}

	.view_more {
		margin-top: 16px;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;

		margin-top: 24px;
	}

	@media screen and (min-width: 580px) {
		.grid {
			gap: 24px;
			grid-template-columns: repeat(3, 1fr);
			/* padding: 24px; */
		}
	}

	@media screen and (min-width: 940px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.item {
		&.can_hide {
			display: none;
		}

		@media screen and (min-width: 940px) {
			&.can_hide {
				display: block;
			}
		}
	}
</style>
