<script>
	export let variation;

	let label = [];
	let color = '';
	let size = '';
	for (let i in variation) {
		if (i == 'size') {
			size = variation[i];
		} else {
			let temp = variation[i].split(':');
			if (temp[1]) {
				color = temp[1];
			}
			temp[0] = temp[0].trim();
			if (temp[0]) {
				label.push(temp[0]);
			}
		}
	}
	label = label.join(', ');
</script>

{#if Object.keys(variation).length !== 0}
	<div class="value" style:background-color={color}>
		{#if label}
			{label}
		{/if}
		{#if label && size}
			:
		{/if}
		{#if size}
			{size}
		{/if}
	</div>
{/if}

<style>
	.value {
		--size: 24px;

		display: flex;
		justify-content: center;
		align-items: center;

		min-width: var(--size);
		height: var(--size);

		font-size: x-small;

		padding: 0 var(--sp1);
		border-radius: calc(var(--size) / 2);

		color: var(--ac5_);
		background-color: var(--ac5);
	}
</style>
