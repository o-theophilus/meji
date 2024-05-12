<script>
	export let card = false;
</script>

<div class="component" class:card>
	<div class="row space_out">
		<div class="row">
			<slot name="left" />
			<div>
				<div class="name">
					<slot />
				</div>
				<slot name="down" />
			</div>
		</div>
		<div class="row">
			<slot name="right" />
		</div>
	</div>
</div>

<style>
	.component {
		margin-top: var(--sp4);
		margin-bottom: var(--sp2);
	}

	.card {
		margin-top: 0;
	}

	.row {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}

	.space_out {
		justify-content: space-between;
	}

	.name {
		font-weight: 900;
		font-size: large;
		color: var(--ac1);
		fill: currentColor;
	}
</style>
