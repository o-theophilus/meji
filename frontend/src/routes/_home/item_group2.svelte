<script>
	import One from '../shop/item.svelte';
	let { items = [], _title, id = '' } = $props();
</script>

{#if items.length > 0}
	<section>
		<div {id}></div>
		<div class="title">
			{@render _title?.()}
		</div>

		<div class="scroller">
			{#each items as item}
				<div class="item">
					<One {item}></One>
				</div>
			{/each}
		</div>
	</section>
{/if}

<style>
	section {
		position: relative;
		z-index: 0;

		margin-top: 120px;
		/* background-color: var(--bg2); */
		background-color: var(--bg);
		border-radius: 24px;
		overflow: hidden;
		/* padding: 40px 0; */
		outline: 1px solid var(--ol);
		outline-offset: -1px;

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
		position: absolute;
		top: 40px;
		left: 0;
		right: 0;

		display: flex;
		flex-direction: column;
		align-items: center;
		pointer-events: none;
	}

	.scroller {
		display: flex;
		gap: 8px;

		padding-top: 120px;
		padding-bottom: 80px;
		padding-left: 16px;
		padding-right: 16px;
		overflow-x: auto;

		@media screen and (min-width: 580px) {
			& {
				padding-left: 40px;
				padding-right: 40px;
			}
		}

		&::-webkit-scrollbar {
			display: none;
		}
	}

	.item {
		flex: 0 0 50%;

		@media screen and (min-width: 580px) {
			& {
				flex: 0 0 200px;
			}
		}
	}
</style>
