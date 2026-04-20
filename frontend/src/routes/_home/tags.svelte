<script>
	import { page_state } from '$lib/store.svelte.js';
	let tags = ['Furniture', 'Fashion', 'Shoe'];
</script>

{#if tags.length > 0}
	<section>
		<div class="title">Shop for furnitures, clothings and more</div>

		<div class="block">
			{#each tags as tag, i}
				<button onclick={() => page_state.goto('shop', { tag })}>
					<img src="/image/item_{i + 1}.png" alt="" />
					<div>
						{tag}
						<div class="shop">Shop Now</div>
					</div>
				</button>
			{/each}
		</div>
	</section>
{/if}

<style>
	section {
		max-width: 800px;
		margin: 160px auto;
		text-align: center;
	}
	.block {
		display: flex;
		margin-top: 24px;
		gap: 8px;

		@media screen and (min-width: 580px) {
			& {
				gap: 16px;
			}
		}
	}

	.title{
		font-size: 2rem;
		font-weight: 600;
		color: var(--ft1);
	}
	button {
		all: unset;
		cursor: pointer;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;

		width: 100%;
		aspect-ratio: 1;
		border-radius: 10%;
		padding: 16px;

		background-color: var(--bg3);
		text-decoration: none;
		color: var(--ft2);

		&:hover {
			background-color: var(--bg2);

			& img {
				width: 70%;
			}
		}

		& img {
			width: 70%;
			aspect-ratio: 1;
			transition: width 0.2s ease-in-out;
		}
	}

	.shop {
		color: var(--cl1);
		font-weight: 800;
		font-size: 0.9rem;
	}
</style>
