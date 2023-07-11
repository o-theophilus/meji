<script>
	import { goto } from '$app/navigation';

	export let size = '300x300';
	export let ads = [];

	let index = 0;

	const auto_scroll = () => {
		index += 1;
		if (index > ads.length - 1) {
			index = 0;
		}
	};

	let timer = setInterval(auto_scroll, 1000 * 5);
	const reset_timer = () => {
		clearInterval(timer);
		timer = setInterval(auto_scroll, 1000 * 5);
	};
</script>

{#if ads.length > 0}
	<section>
		<img
			src={ads[index].ads[size]}
			alt={ads[index].name}
			on:keypress
			on:click={() => {
				goto(`/${ads[index].alias}`);
			}}
		/>

		{#if ads.length > 1}
			<div class="control">
				{#each ads as _, i}
					<div
						class="btn"
						class:active={index == i}
						on:keypress
						role="button"
						tabindex="0"
						on:click={() => {
							index = i;
							reset_timer();
						}}
					/>
				{/each}
			</div>
		{/if}
	</section>
{/if}

<style>
	section {
		display: flex;
		position: relative;
		box-shadow: var(--shad1);
		border-radius: var(--brad1);
		overflow: hidden;
	}

	img {
		width: 100%;
		cursor: pointer;
	}

	.control {
		position: absolute;
		bottom: 24px;

		display: flex;
		gap: var(--sp1);
		justify-content: center;

		width: 100%;
	}

	.btn {
		--size: 20px;

		width: var(--size);
		height: var(--size);

		border-radius: var(--size);

		background-color: var(--cl1);

		transition: var(--trans1);
	}

	.btn:hover {
		width: calc(var(--size) * 2.5);
	}

	.btn.active {
		width: calc(var(--size) * 2.5);
	}
</style>
