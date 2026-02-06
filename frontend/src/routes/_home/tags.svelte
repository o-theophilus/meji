<script>
	import { module, page_state } from '$lib/store.svelte.js';
	import { LinkArrow, Button } from '$lib/button';
	import { Content, Card } from '$lib/layout';
	import { Icon } from '$lib/macro';

	tags = ['male', 'palm', 'female'];
</script>

{#if tags.length > 0}
	<section>
		<div class="page_title">Shop devices, accessories and more from the Meji</div>

		<div class="block">
			{#each tags as tag, i}
				<a href="/shop?tag={tag}">
					<img src="/image/item_{i + 1}.png" alt="" />
					<div>
						{tag}
						<div class="shop">Shop Now</div>
					</div>
				</a>
			{/each}
		</div>
	</section>
{/if}

<style>
	section {
		max-width: 720px;
		margin: auto;
		margin-top: 16px;
		text-align: center;
	}
	.block {
		display: flex;
		margin-top: 24px;
		gap: 16px;
	}

	a {
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
